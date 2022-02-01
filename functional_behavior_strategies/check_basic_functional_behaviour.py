"""
this strategy takes input directory and run the inputs
and check the output if undefined behaviour from sanitizer
is detected
"""
import os
import subprocess
import random
import pathlib

STRATEGY_NAME = "check_basic_functional_behaviour"


def run_strategy(input_path, SUT_path, seed, bugs_logs_path):
    """
    Picks a random .cnf file from the functional_inputs dir, finds if its satisfiable
    and feed it to the SUT to check if their are functional behaviour errors.

    :return:
    """
    sat_flag = 0  # 1 - SAT & 0 - UNSAT
    inputs_path = "inputs/functional_inputs"
    if not os.path.exists(inputs_path):
        print("[!] Input path given does not exist")
        return
    input_files = [f for f in os.listdir(inputs_path) if os.path.join(inputs_path, f)]
    # input_file = random.choice(input_files)
    # print(input_file)
    for i_file in input_files:
        current_file = os.path.abspath(os.path.join(inputs_path, i_file))
        output, error = run_program(current_file, SUT_path, seed, bugs_logs_path)
        if error != "":
            log_error_case(i_file, SUT_path, bugs_logs_path, '\n'.join(output), '\n'.join(error))
            continue
        if "yes" in i_file and output != "" and output[1] != "SAT":
            log_error_case(i_file, SUT_path, bugs_logs_path, '\n'.join(output),
                           '\n'.join(error) + "\nthe solver should yield a satisfiable solution")
        elif "no" in i_file and output != "" and output[1] != "UNSAT":
            log_error_case(i_file, SUT_path, bugs_logs_path, '\n'.join(output),
                           '\n'.join(error) + "\nthe solver should yield a unsatisfiable solution")


def run_program(input_path, SUT_path, seed, bugs_logs_path):
    result = subprocess.Popen(["./runsat.sh", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=SUT_path)
    try:
        sut_output, sut_error = result.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        result.kill()
        sut_output, sut_error = result.communicate()
        return sut_output, "time out in 20 sec"

    sut_output_printable = sut_output.decode('ascii', 'replace').split('\n')
    sut_output_error = sut_error.decode('ascii', 'replace').split('\n')
    print(f"running {input_path}")
    print("normal output")
    print('\n'.join(sut_output_printable))
    # print(f"error output")
    # print('\n'.join(sut_output_error))

    return sut_output_printable, sut_output_error


def log_error_case(input_file, SUT_path, bugs_logs_path, output, error):
    sut_dir = os.path.join(bugs_logs_path, os.path.basename(os.path.normpath(SUT_path)))
    strategy_dir = os.path.join(sut_dir, STRATEGY_NAME)
    pathlib.Path(strategy_dir).mkdir(parents=True, exist_ok=True)

    # create log of the bug
    full_path = os.path.join(strategy_dir, f"{os.path.basename(os.path.normpath(input_file))}.txt")
    file = open(full_path, "w")
    file.write(f"[!] False input file {input_file} the error found is:\n")
    file.write(error)
    file.write("----------------------------------------------------------")
    file.write(output)
    file.close()
