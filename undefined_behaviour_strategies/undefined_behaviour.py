'''
the file contains the functions responsible to run the startgies
to detetct undefined behviour
'''
import os
from  undefined_behaviour_strategies import simple_sanatizer_undefined_behviour
from undefined_behaviour_strategies import false_file_input_undefined_behivour
# array of startgies to be run 
stratgies = {
    simple_sanatizer_undefined_behviour.STRATEGY_NAME :simple_sanatizer_undefined_behviour.run_strategy,
    false_file_input_undefined_behivour.STRATEGY_NAME:false_file_input_undefined_behivour.run_strategy
}
def run_stragies(input_path,SUT_path,seed,bugs_logs_path):
        for current_strategy_name,current_strategy_func  in stratgies.items():
            print(f"running {current_strategy_name} strategy")
            current_strategy_func(input_path,SUT_path,seed,bugs_logs_path)
            print(f"end of running {current_strategy_name}strategy")
            print()


