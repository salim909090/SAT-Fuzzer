import random
from mutation import fuzzing_data_random
import numpy as np
import sys
def generate_smart_cnf():
    # choice of insert random comment or not
    comment_choice = random.choice([0,1])
    cnf = ""
    if comment_choice:
        cnf += "c " + fuzzing_data_random(0,100).replace("\n","") + "\n"
    
    # big or small number of vars
    big_small_var_number = random.choice([0,1,2])
    var_number =0
    if big_small_var_number == 0:
        var_number = random.randint(0,10)
    elif big_small_var_number == 1:
        var_number = random.randint(10,100)
    elif big_small_var_number == 2:
        var_number = random.randint(1000,10000)

    # big or small number of args
    big_small_arg_number = random.choice([0,1,2])
    arg_number =0
    if big_small_arg_number == 0:
        arg_number = random.randint(0,10)
    elif big_small_arg_number == 1:
        arg_number = random.randint(10,100)
    elif big_small_arg_number == 2:
        arg_number = random.randint(1000,10000)

    cnf += f"p cnf {var_number} {arg_number}\n" 

    # use all args?
    use_all_args_number = random.choice([0,1])

    # use all vars?
    use_all_vars_number = random.choice([0,1])

    # forget 0 at end of line
    forget_0_ending = random.choice([0,1])

    # insert out of range var
    out_of_range_var = random.choice([0,1])

    # can leave empty spaces
    leave_empty_Space = random.choice([0,1])

    # list of vars available
    vars = list(range(1,var_number+1))
    if not use_all_vars_number:
        skiped_vars = random.randint(0,var_number)
        vars = delete_random_elems(vars,skiped_vars)

    if out_of_range_var:
        vars.append(var_number+random.randint(var_number+1,sys.maxsize))

    for current_arg in range(arg_number):
        if not use_all_args_number:
            skip_current_arg =  random.choice([0,1])
            if skip_current_arg:
                # skip arg
                continue

        # write arg
        numb_vars = random.randint(0,len(vars))
        vars_to_be_in_arg = random.sample(vars,numb_vars)
        if numb_vars == 0:
            leave_empty_space = random.choice([0,1])
            if leave_empty_space and leave_empty_Space:
                cnf += "\n"
        else:
            numb_neg_vars = random.randint(0,numb_vars)
            neg_vars = random.sample(vars_to_be_in_arg,numb_neg_vars)
            neg_vars = np.negative(neg_vars)
            pos_vars = list(set(vars_to_be_in_arg) - set(neg_vars))

            str_neg_vars = [str(int) for int in neg_vars]
            str_pos_vars = [str(int) for int in pos_vars]
            
            cnf += " ".join(str_neg_vars) + " " +  " ".join(str_pos_vars)
            if forget_0_ending:
                forget_0_current = random.choice([0,1])
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
    return [x for i,x in enumerate(input_list) if not i in to_delete]
    
while True:
    print(generate_smart_cnf())
    sys.stdout.flush()
