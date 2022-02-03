'''
this strategy supply false directory inputs and check
if the application handle wrong input directory
'''
from lib2to3.pgen2.token import STAR
import os
import subprocess
import random
import pathlib
import time
import textdistance
import shutil
STRATEGY_NAME = "false_file_inputs_check"
interesting_behaviours_encountered = []

def run_strategy(input_path,SUT_path,seed,bugs_logs_path,input_bugs):
    bugs_counter = 0
    input_File,output,error = run_program(SUT_path,seed,bugs_logs_path)
    if error is not None:
        values = [textdistance.levenshtein.normalized_similarity(error, current) for current in interesting_behaviours_encountered]
        if len(values) == 0 or max(values) < 0.2:
            interesting_behaviours_encountered.append(error)
            log_error_case(input_File,SUT_path,bugs_logs_path,input_bugs,output,error)
            bugs_counter += 1

    return bugs_counter

def run_program (SUT_path,seed,bugs_logs_path):
    input_path = generate_input(seed)
    result = subprocess.Popen(["./runsat.sh", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=SUT_path)

    try:
        sut_output, sut_error = result.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        result.kill()
        return input_path,"","time out in 10 sec"

    sut_output_printable = sut_output.decode('ascii','replace')
    sut_output_error = sut_error.decode('ascii','replace')
    if sut_output_error.strip() != "":
        return input_path,sut_output_printable,sut_output_error
    return input_path, sut_output_printable, None

def generate_input(seed):
    if random.choice([0,1]):
        return ''

    input = ''
    length = random.randint(0,50)
    for current_input in range(length):
        input += chr(random.randrange(33,126))
    input = input.replace('\n','').replace('\x00','')

    if random.choice([0,1]):
        second_input = ''
        length = random.randint(0,50)
        for current_input in range(length):
            second_input += chr(random.randrange(33,126))
        secound_input = second_input.replace('\n','').replace('\x00','')
        input += " " + secound_input

    return input

def log_error_case(input_file, SUT_path, bugs_logs_path,input_bugs, output, error):
    sut_name = os.path.basename(os.path.normpath(SUT_path))
    sut_dir = os.path.join(bugs_logs_path, sut_name)
    strategy_dir = os.path.join(sut_dir, STRATEGY_NAME)
    pathlib.Path(strategy_dir).mkdir(parents=True, exist_ok=True)
    dst = os.path.join(os.path.abspath(input_bugs),sut_name,STRATEGY_NAME)
    pathlib.Path(dst).mkdir(parents=True, exist_ok=True)

    # copy input to fuzzed tests directory
    input_bugs_sut_path = os.path.join(input_bugs,sut_name,STRATEGY_NAME,f"{os.path.basename(os.path.normpath(input_file))}.txt")
    file = open(input_bugs_sut_path, "w")
    file.write(f"[!] False input file {input_file} the error found is:\n")
    file.write("std output:\n")
    file.write(output+"\n")
    file.write("std error\n")
    file.write(error)
    file.close()

    # create log of the bug
    full_path = os.path.join(strategy_dir, f"{os.path.basename(os.path.normpath(input_file))}.txt")
    file = open(full_path, "w")
    file.write(f"[!] False input file {input_file} the error found is:\n")
    file.write("std output:\n")
    file.write(output+"\n")
    file.write("std error\n")
    file.write(error)
    file.close()