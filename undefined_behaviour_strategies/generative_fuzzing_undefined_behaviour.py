"""
this strategy generate input in dumb (random) and smart (making use of the format)
"""
import os
import subprocess
import pathlib
import random
import numpy as np
import sys
import Levenshtein
import corpus_tracker
import mutation
from mutation import fuzzing_data_random
import textdistance
import shutil
STRATEGY_NAME = "generative_fuzzing"
interesting_behaviours_encountered = []


def run_strategy(input_path, SUT_path, seed, bugs_logs_path,input_bugs):
    # probability 50 ,50 smart and dumb input
    corpus = corpus_tracker.Corpus.get_instance()
    if corpus.queue_is_empty("ub"):
        dumb_smart_choice = random.choice([0,1])
        if dumb_smart_choice == 0:
            input_data = generate_dumb_cnf()
        else:
            input_data = generate_smart_cnf()
    else:
        input_file = corpus.pop_queue("ub")
        file1 = open(input_file, "r+")
        input_data = mutation.mutate(file1.read())
        #input_data = corpus.pop_queue("ub")
    file_name_full_path = os.path.abspath(os.path.join(input_path))
    file_name = os.path.basename(os.path.normpath(file_name_full_path))
    create_input_file(file_name_full_path, input_data)
    before_coverage = corpus.find_coverage(SUT_path, file_name_full_path, "ub", 20)

    output,error = run_program(file_name_full_path, SUT_path, seed, bugs_logs_path)
    corpus.find_coverage(SUT_path, file_name_full_path, "ub", 20)
    bug_counter = 0

    if error is not None:
        values = [textdistance.levenshtein.normalized_similarity(error, current) for current in interesting_behaviours_encountered]

        if len(values) == 0:
            interesting_behaviours_encountered.append(error)
            log_error_case(file_name_full_path, SUT_path, bugs_logs_path,input_bugs, output,error)
            bug_counter +=1
        elif max(values) < 0.5:
            bug_counter += 1
            interesting_behaviours_encountered.append(error)
            log_error_case(file_name_full_path, SUT_path, bugs_logs_path,input_bugs, output,error)
        if corpus.current_coverage > before_coverage:
            corpus.add_cnf(file_name_full_path,"ub",20)
    return bug_counter

def generate_dumb_cnf():
    # choice short or long input
    short_long_choice = random.choice([0, 1])
    if short_long_choice == 0:
        return fuzzing_data_random(0, 100)
    else:
        return fuzzing_data_random(1000, 10000)


def generate_smart_cnf():
    # choice of insert random comment or not
    comment_choice = random.choice([0, 1])
    cnf = ""
    # if comment_choice:
    #     cnf += "c " + fuzzing_data_random(0,100).replace("\n","") + "\n"

    # big or small number of vars
    big_small_var_number = random.choice([0,1, 2])
    var_number = 0
    if big_small_var_number == 0:
        var_number = random.randint(0, 10)
    elif big_small_var_number == 1:
        var_number = random.randint(10, 100)
    elif big_small_var_number == 2:
        var_number = random.randint(100, 500)

    # big or small number of args
    big_small_arg_number = random.choice([0, 1, 2])
    arg_number = 0
    if big_small_arg_number == 0:
        arg_number = random.randint(0, 10)
    elif big_small_arg_number == 1:
        arg_number = random.randint(10, 100)
    elif big_small_arg_number == 2:
        arg_number = random.randint(100, 500)

    cnf += f"p cnf {var_number} {arg_number}\n"
    # fully valid or abuse format
    valid_abuse = random.choice([0, 1])
    if valid_abuse:  # valid
        use_all_args_number = 1
        use_all_vars_number = 1
        forget_0_ending = 0
        out_of_range_var = 0
        leave_empty_Space = 0
        replace_char_var = 0
        replace_float_var = 0
    else:  # abuse
        # use all args?
        use_all_args_number = random.choice([0, 1])

        # use all vars?
        use_all_vars_number = random.choice([0, 1])

        # forget 0 at end of line
        forget_0_ending = random.choice([0, 1])

        # insert out of range var
        out_of_range_var = random.choice([0, 1])

        # can leave empty spaces
        leave_empty_Space = random.choice([0, 1])

        # add char rather than int for var
        replace_char_var = random.choice([0, 1])

        # add float rather than int for var
        replace_float_var = random.choice([0, 1])

    # list of vars available
    vars = list(range(1, var_number + 1))
    if not use_all_vars_number:
        skiped_vars = random.randint(0, var_number)
        vars = delete_random_elems(vars, skiped_vars)

    if out_of_range_var:
        vars.append(var_number + random.randint(var_number + 1, sys.maxsize))

    for current_arg in range(arg_number):
        if not use_all_args_number:
            skip_current_arg = random.choice([0, 1])
            if skip_current_arg:
                # skip arg
                continue

        # write arg
        numb_vars = random.randint(0, len(vars))
        vars_to_be_in_arg = random.sample(vars, numb_vars)
        if numb_vars == 0:
            current_leave_empty_space = random.choice([0, 1])
            if current_leave_empty_space and leave_empty_Space:
                cnf += "\n"
        else:
            numb_neg_vars = random.randint(0, numb_vars)
            neg_vars = random.sample(vars_to_be_in_arg, numb_neg_vars)
            neg_vars = np.negative(neg_vars)
            pos_vars = list(set(vars_to_be_in_arg) - set(neg_vars))

            str_neg_vars = [str(int) for int in neg_vars]
            str_pos_vars = [str(int) for int in pos_vars]

            cnf += " ".join(str_neg_vars) + " " + " ".join(str_pos_vars)

            if replace_char_var and random.choice([0, 1]):
                cnf += " " + fuzzing_data_random(1, 20)

            if replace_float_var and random.choice([0, 1]):
                cnf += " " + str(random.random() * 10)

            if forget_0_ending:
                forget_0_current = random.choice([0, 1])
                if forget_0_current:
                    # forget 0
                    cnf += "\n"
                else:
                    cnf += " 0\n"
            else:
                cnf += " 0\n"

    return cnf


def delete_random_elems(input_list, n):
    to_delete = set(random.sample(range(len(input_list)), n))
    return [x for i, x in enumerate(input_list) if not i in to_delete]


def create_input_file(abs_file_path, input_data):
    file = open(abs_file_path, "w")
    file.write(input_data)
    file.close()


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
    if sut_output_error.strip() != "":
        return sut_output_printable,sut_output_error
    return sut_output_printable,None

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
