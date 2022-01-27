'''
the file contains the functions responsible to run the startgies
to detetct wrong functional behviour
'''
from functional_behavior_strategies import check_basic_functional_behviour
# array of startgies to be run 
stratgies = {
    check_basic_functional_behviour.STRATEGY_NAME:check_basic_functional_behviour.run_strategy


}

def run_stargies(input_path,SUT_path,seed,bugs_logs_path):
        for current_strategy_name,current_strategy_func  in stratgies.items():
            print(f"running {current_strategy_name} strategy")
            current_strategy_func(input_path,SUT_path,seed,bugs_logs_path)
            print(f"end of running {current_strategy_name}strategy")
            print()
