"""
this strategy takes input directory and run the inputs
and check the output if undefined behaviour from sanitizer
is detected
"""
import os
import subprocess
import random
import pathlib
import time
import shutil
import psutil
import textdistance


STRATEGY_NAME = "check_basic_functional_behaviour"
interesting_behaviours_encountered = []


def run_strategy(input_path, SUT_path, seed, bugs_logs_path,input_bugs):
    """
    Picks a random .cnf file from the functional_inputs dir, finds if its satisfiable
    and feed it to the SUT to check if their are functional behaviour errors.

    :return:
    """
    sat_flag = 0  # 1 - SAT & 0 - UNSAT
    inputs_path = os.path.join(input_path ,"functional_inputs")
    if not os.path.exists(inputs_path):
        print(f"[!] Input path {inputs_path} given does not exist")
        return
    
    input_files = [f for f in os.listdir(inputs_path) if os.path.join(inputs_path, f)]
    start = time.time()
    end = print_status(start,0,len(input_files),0)
    counter_files = 0
    total_files = len(input_files)
    bugs_counter = 0
    for i_file in input_files:

        full_input_path = os.path.abspath(os.path.join(inputs_path,i_file))
        counter_files += 1
        end = print_status(start,counter_files,total_files, bugs_counter)
        current_file = os.path.abspath(os.path.join(inputs_path, i_file))
        output, error = run_program(current_file, SUT_path)
        error =[x for x in error if x]

        if len(error) > 0 and not error[0].startswith("time out"):
            values = [textdistance.levenshtein.normalized_similarity(error, current) for current in interesting_behaviours_encountered]
            if len(interesting_behaviours_encountered) == 0:
                interesting_behaviours_encountered.append('\n'.join(error))
                log_error_case(full_input_path, SUT_path, bugs_logs_path,input_bugs, '\n'.join(output), '\n'.join(error))
                bugs_counter += 1
            elif max(values) < 0.5:
                interesting_behaviours_encountered.append('\n'.join(error))
                log_error_case(full_input_path, SUT_path, bugs_logs_path,input_bugs, '\n'.join(output), '\n'.join(error))
                bugs_counter += 1

        if "yes" in i_file and len(output) > 0 and output[0] != "SAT":
            error_msg = "the solver should yield a satisfiable solution"
            if len(interesting_behaviours_encountered) == 0:
                interesting_behaviours_encountered.append("the solver should yield a satisfiable solution")
                log_error_case(full_input_path, SUT_path, bugs_logs_path,input_bugs, '\n'.join(output),
                           '\n'.join(error) + "\nthe solver should yield a satisfiable solution")
                bugs_counter += 1
            elif error_msg not in interesting_behaviours_encountered:
                interesting_behaviours_encountered.append("the solver should yield a satisfiable solution")
                log_error_case(full_input_path, SUT_path, bugs_logs_path,input_bugs, '\n'.join(output),
                           '\n'.join(error) + "\nthe solver should yield a satisfiable solution")
                bugs_counter += 1

        elif "no" in i_file and len(output) > 0 and output[0] != "UNSAT":
            error_msg = "the solver should yield a unsatisfiable solution"
            if len(interesting_behaviours_encountered) == 0:
                interesting_behaviours_encountered.append("the solver should yield a unsatisfiable solution")
                log_error_case(full_input_path, SUT_path, bugs_logs_path,input_bugs, '\n'.join(output),
                           '\n'.join(error) + "\nthe solver should yield a unsatisfiable solution")
                bugs_counter += 1
            elif error_msg not in interesting_behaviours_encountered:
                interesting_behaviours_encountered.append("the solver should yield a unsatisfiable solution")
                log_error_case(full_input_path, SUT_path, bugs_logs_path,input_bugs, '\n'.join(output),
                           '\n'.join(error) + "\nthe solver should yield a unsatisfiable solution")
                bugs_counter += 1

    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "Runtime: {:0>2}:{:05.2f}".format(int(minutes), seconds) + f", Bugs Found: {bugs_counter}"

def print_status(start,current_file,total_file,bugs_found):
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    statistics = {}

    # Get Physical and Logical CPU Count
    physical_and_logical_cpu_count = os.cpu_count()
    statistics['physical_and_logical_cpu_count'] = physical_and_logical_cpu_count
    cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]
    statistics['cpu_load'] = cpu_load
    print("Runtime: {:0>2}:{:05.2f}".format(int(minutes), seconds) + f", Memory: " + str(psutil.virtual_memory().percent)+f" Running {current_file} out of {total_file} inputs, " + f" Bugs found {bugs_found}",end='\r')
    return end



def run_program(input_path, SUT_path):
    result = subprocess.Popen(['timeout' ,'10',"./runsat.sh", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=SUT_path)
    try:
        sut_output, sut_error = result.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        result.kill()
        return [""],["time out in 10 sec"]
    sut_output_printable = list(sut_output.decode('ascii', 'replace').split('\n'))
    sut_output_error = list(sut_error.decode('ascii', 'replace').split('\n'))

    return sut_output_printable, sut_output_error


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
    file.write(f"[!] False input file {input_file} the error found is:\n")
    file.write("std output:\n")
    file.write(output+"\n")
    file.write("std error\n")
    file.write(error)
    file.close()
