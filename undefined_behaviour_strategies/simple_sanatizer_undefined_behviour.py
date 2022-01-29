"""
this stratgy takes input directory and run the inputs
and check the output if undefined behviour from sanatizor
is detected
"""
import os
import subprocess
import pathlib
import corpus_tracker

from pathlib import Path

STRATEGY_NAME = "sanatizer_undefined_behaviour_fuzzing"


def run_strategy(input_path, SUT_path, seed, bugs_logs_path):
    corpus = corpus_tracker.Corpus.get_instance()
    print("test2")
    while not corpus.queue_is_empty("ub"):
        file_name_full_path = corpus.pop_queue("ub")
        current_input_filename = Path(file_name_full_path).name
        error = run_program(file_name_full_path, SUT_path, seed, bugs_logs_path)
        if error is not None:
            log_error_case(current_input_filename, file_name_full_path, SUT_path, bugs_logs_path, error)


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
    for line in sut_output_printable:
        print(line)
        break

    print("error output")
    for line in sut_output_error:
        if "ERROR" in line:
            # print(line)
            print(' '.join(line.split(" ")[:3]))
            print(f"end of running {input_path}")
            print()
            return '\n'.join(sut_output_error)

    print(f"end of running {input_path}")
    print()
    return None


def log_error_case(current_input_filename, file_name_full_path, SUT_path, bugs_logs_path, error):
    # create dir and strategy dir if does not exist
    sut_dir = os.path.join(bugs_logs_path, os.path.basename(os.path.normpath(SUT_path)))
    strategy_dir = os.path.join(sut_dir, STRATEGY_NAME)
    pathlib.Path(strategy_dir).mkdir(parents=True, exist_ok=True)

    # create log of the bug
    full_path = os.path.join(strategy_dir, f"{current_input_filename}.txt")
    file = open(full_path, "w")
    file.write(f"input file taken from {file_name_full_path} the error found is:\n")
    file.write(error)
    file.close()
