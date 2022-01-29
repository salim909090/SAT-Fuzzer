'''
the file contains the functions responsible to run the startgies
to detetct undefined behviour
'''
import os
from  undefined_behaviour_strategies import simple_sanatizer_undefined_behviour
from undefined_behaviour_strategies import false_file_input_undefined_behivour

from undefined_behaviour_strategies import generative_fuzzing_undefined_behviour
import Levenshtein
import pathlib
import corpus_tracker

# array of startgies to be run 

# array of startgies to be run 
strategies = {
    simple_sanatizer_undefined_behviour.STRATEGY_NAME :simple_sanatizer_undefined_behviour.run_strategy,
    false_file_input_undefined_behivour.STRATEGY_NAME:false_file_input_undefined_behivour.run_strategy
}

def run_strategies(input_path,SUT_path,seed,bugs_logs_path):
        corpus = corpus_tracker.Corpus.getInstance()
        corpus.initialise_queue(input_path,"ub")
        for current_strategy_name,current_strategy_func in strategies.items():
            print(f"running {current_strategy_name} strategy")
            current_strategy_func(input_path,SUT_path,seed,bugs_logs_path)
            print(f"end of running {current_strategy_name}strategy")
            print()

        counter = 0
        print(f"running {generative_fuzzing_undefined_behviour.STRATEGY_NAME} strategy")
        # create input directory
        sut_name = os.path.basename(os.path.normpath(SUT_path))
        pathlib.Path(os.path.join(input_path,sut_name,generative_fuzzing_undefined_behviour.STRATEGY_NAME)).mkdir(parents=True, exist_ok=True)
        while True:
            full_input_file_path = os.path.join(input_path,sut_name,generative_fuzzing_undefined_behviour.STRATEGY_NAME,f"{counter}.cnf")
            generative_fuzzing_undefined_behviour.run_strategy(full_input_file_path,SUT_path,seed,bugs_logs_path)
            counter += 1


