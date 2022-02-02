'''
this strategy supply false directory inputs and check
if the application handle wrong input directory
'''
import os
import subprocess
import random
import pathlib

STRATEGY_NAME = "false_file_inputs_check"
def run_strategy(input_path,SUT_path,seed,bugs_logs_path):
    error,input = run_program(SUT_path,seed,bugs_logs_path)
    if error is not None:
        log_error_case(input,SUT_path,bugs_logs_path,error)

def run_program (SUT_path,seed,bugs_logs_path):
    input_path = generate_input(seed)
    result = subprocess.Popen(["./runsat.sh", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=SUT_path)

    try:
        sut_output, sut_error = result.communicate(timeout=40)
    except subprocess.TimeoutExpired:
        result.kill()
        sut_output, sut_error = result.communicate()
        return "time out in 20 sec",input


    sut_output_printable = sut_output.decode('ascii','replace').split('\n')
    sut_output_error = sut_error.decode('ascii','replace').split('\n')
    print(f"running {input_path}")
    print("normal output")
    for line in sut_output_printable:
        print(line)
        break

    print("error output")
    counter =0
    for line in sut_output_error:
        if "ERROR" in line:    
            # print(line)
            print(' '.join(line.split(" ")[:3]))
            print(f"end of running {input_path}")
            print()
            return '\n'.join(sut_output_error),input

    print(f"end of running {input_path}")
    print()
    return None,input

def generate_input(seed):
    input = ''
    length = random.randint(0,150)
    for current_input in range(length):
        input += chr(random.randrange(0,256))
    input = input.replace('\n','').replace('\x00','')

    if random.choice([0,1]):
        second_input = ''
        length = random.randint(0,150)
        for current_input in range(length):
            second_input += chr(random.randrange(0,256))
        secound_input = second_input.replace('\n','').replace('\x00','')
        input += " " + secound_input

    return input

def log_error_case(input,SUT_path,bugs_logs_path,error):
    sut_dir = os.path.join(bugs_logs_path,os.path.basename(os.path.normpath(SUT_path)))
    strategy_dir = os.path.join(sut_dir,STRATEGY_NAME)
    pathlib.Path(strategy_dir).mkdir(parents=True, exist_ok=True)

    # create log of the bug
    full_path = os.path.join(strategy_dir,"false_file_input.txt")
    file = open(full_path, "w")
    file.write(f"false input file {input} the error found is:\n")
    file.write(error)
    file.close()