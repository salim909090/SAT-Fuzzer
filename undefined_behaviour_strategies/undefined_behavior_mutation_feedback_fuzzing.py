"""
This strategy takes input directory and run the inputs
and check the output if undefined behaviour from sanitizer
is detected.
"""
import os
import subprocess
import pathlib
import corpus_tracker
import time
from pathlib import Path
import psutil
import shutil
import textdistance

STRATEGY_NAME = "undefined_behavior_mutation_feedback_fuzzing"
interesting_behaviours_encountered = []


def run_strategy(input_path, SUT_path, seed, bugs_logs_path,input_bugs):
    start = time.time()
    corpus = corpus_tracker.Corpus.get_instance()

    end = print_status(start,0,0,corpus.current_coverage)

    counter_mutations = 0
    bugs_counter = 0
    while not corpus.queue_is_empty("ub"):
        file_name_full_path = corpus.pop_queue("ub")

        counter_mutations += 1
        corpus.find_coverage(SUT_path, file_name_full_path, "ub", 20)
        before_coverage = corpus.current_coverage
        end = print_status(start,counter_mutations, bugs_counter,corpus.current_coverage)
        current_input_filename = Path(file_name_full_path).name
        output,error = run_program(file_name_full_path, SUT_path, seed, bugs_logs_path)
        if error is not None and not error.startswith("time out"):
            values = [textdistance.levenshtein.normalized_similarity(error, current) for current in interesting_behaviours_encountered]
            if len(values) == 0 or max(values) < 0.5:
                interesting_behaviours_encountered.append(error)
                log_error_case(file_name_full_path, SUT_path, bugs_logs_path,input_bugs,output, error)
                bugs_counter += 1
            corpus.find_coverage(SUT_path, file_name_full_path, "ub", 20)
            if corpus.current_coverage > before_coverage:
                corpus.add_cnf(file_name_full_path,"ub",20)

        
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)

    return "Runtime: {:0>2}:{:05.2f}".format(int(minutes), seconds) + f", Bugs Found: {bugs_counter}" + f", code coverage: {corpus.current_coverage}"


def run_program(input_path, SUT_path, seed, bugs_logs_path):
    result = subprocess.Popen(["./runsat.sh", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=SUT_path)

    try:
        sut_output, sut_error = result.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        result.kill()
        return "","time out in 10 sec"

    sut_output_printable = sut_output.decode('ascii', 'replace')
    sut_output_error = sut_error.decode('ascii', 'replace')



    for line in sut_output_error:
        if line.strip() != "":
            return sut_output_printable,sut_output_error

    return sut_output_printable,None

def print_status(start,current_file,bugs_found,current_coverage):
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    statistics = {}

    # Get Physical and Logical CPU Count
    physical_and_logical_cpu_count = os.cpu_count()
    statistics['physical_and_logical_cpu_count'] = physical_and_logical_cpu_count
    cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]
    statistics['cpu_load'] = cpu_load
    print("Runtime: {:0>2}:{:05.2f}".format(int(minutes), seconds) + f", Memory: " + str(psutil.virtual_memory().percent)+f" Running input {current_file}, " + f" Bugs found {bugs_found}, " + f"current coverage {current_coverage}",end='\r')
    return end

def log_error_case(input_file, SUT_path, bugs_logs_path,input_bugs, output, error):
    sut_name = os.path.basename(os.path.normpath(SUT_path))
    sut_dir = os.path.join(bugs_logs_path, sut_name)
    strategy_dir = os.path.join(sut_dir, STRATEGY_NAME)
    pathlib.Path(strategy_dir).mkdir(parents=True, exist_ok=True)
    dst = os.path.join(os.path.abspath(input_bugs),sut_name,STRATEGY_NAME)
    pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
    # copy input to fuzzed tests directory
    shutil.copyfile(input_file, os.path.join(dst,os.path.basename(input_file)))

    # create log of the bug
    full_path = os.path.join(strategy_dir, f"{os.path.basename(os.path.normpath(input_file))}.txt")
    file = open(full_path, "w")
    file.write(f"[!] False input file atg given, the error found is:\n")
    file.write("std output:\n")
    file.write(output+"\n")
    file.write("std error\n")
    file.write(error)
    file.close()
