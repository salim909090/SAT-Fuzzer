"""
this strategy takes input directory and run the inputs
and check the output if undefined behaviour from sanitizer
is detected
"""
import os
import subprocess
import random

STRATEGY_NAME = "check_basic_functional_behaviour"


def run_strategy(input_path, SUT_path, seed, bugs_logs_path):
    # check satisfiable
    input_data = generate_satisfiable_cnf()
    file_name_full_path = os.path.abspath(os.path.join(input_path, "satisfiable_cnf.cnf"))
    create_input_file(file_name_full_path, input_data)

    output = run_program(file_name_full_path, SUT_path, seed, bugs_logs_path)

    if not is_satisfiable(output):
        log_error_case("satisfiable_cnf", file_name_full_path, SUT_path, bugs_logs_path,
                       "satisfiable cnf result in unsatisfiable")

    # check unsatisfiable
    input_data = generate_unsatisfiable_cnf()
    file_name_full_path = os.path.abspath(os.path.join(input_path, "unsatisfiable_cnf.cnf"))
    create_input_file(file_name_full_path, input_data)
    output = run_program(file_name_full_path, SUT_path, seed, bugs_logs_path)

    if is_satisfiable(output):
        log_error_case("unsatisfiable_cnf", file_name_full_path, SUT_path, bugs_logs_path,
                       "unsatisfiable cnf result in satisfiable")


# To be merged with rest of code
def pick_random_sat_file():
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
    input_file = random.choice(input_files)
    # print(input_file)
    if "yes" in input_file:
        sat_flag = 1

    # TODO
    # run program with input file
# pick_random_sat_file()

def generate_satisfiable_cnf():
    return "p cnf 1 1\n1 -1 0"


def generate_unsatisfiable_cnf():
    return "p cnf 1 2\n1 0\n-1 0"


def create_input_file(abs_file_path, input_data):
    file = open(abs_file_path, "w")
    file.write(input_data)
    file.close()


def is_satisfiable(output):
    return "SAT" == output


def run_program(input_path, SUT_path, seed, bugs_logs_path):
    result = subprocess.Popen(["./runsat.sh", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=SUT_path)

    try:
        sut_output, sut_error = result.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        result.kill()
        sut_output, sut_error = result.communicate()
        return "time out in 20 sec"

    sut_output_printable = sut_output.decode('ascii', 'replace').split('\n')
    sut_output_error = sut_error.decode('ascii', 'replace').split('\n')
    print(f"running {input_path}")
    print("normal output")
    print('\n'.join(sut_output_printable))
    return sut_output_printable[0]


def log_error_case(current_input_filename, file_name_full_path, SUT_path, bugs_logs_path, error):
    # create dir and strategy dir if does not exist
    if not os.path.exists(bugs_logs_path):
        os.makedirs(bugs_logs_path)

    sut_dir = os.path.join(bugs_logs_path, os.path.basename(os.path.normpath(SUT_path)))
    if not os.path.exists(sut_dir):
        os.makedirs(sut_dir)
    strategy_dir = os.path.join(sut_dir, STRATEGY_NAME)
    if not os.path.exists(strategy_dir):
        os.makedirs(strategy_dir)

    # create log of the bug
    full_path = os.path.join(strategy_dir, f"{current_input_filename}.txt")
    file = open(full_path, "w")
    file.write(f"[!] Input file taken from {file_name_full_path} the error found is:\n")
    file.write(error)
    file.close()