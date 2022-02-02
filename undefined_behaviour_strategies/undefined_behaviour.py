"""
the file contains the functions responsible to run the startgies
to detetct undefined behviour
"""
import os
# import Levenshtein
import pathlib
import corpus_tracker

from undefined_behaviour_strategies import simple_sanitizer_undefined_behaviour
from undefined_behaviour_strategies import false_file_input_undefined_behaviour
from undefined_behaviour_strategies import generative_fuzzing_undefined_behaviour

# array of strategies to be run
strategies = {
    simple_sanitizer_undefined_behaviour.STRATEGY_NAME: simple_sanitizer_undefined_behaviour.run_strategy,
    false_file_input_undefined_behaviour.STRATEGY_NAME: false_file_input_undefined_behaviour.run_strategy
}


def run_strategies(input_path, SUT_path, seed, bugs_logs_path):
    corpus = corpus_tracker.Corpus.get_instance()
    corpus.initialise_queue(input_path, "ub", 1)
    print("test")

    for current_strategy_name, current_strategy_func in strategies.items():
        print(f"running {current_strategy_name} strategy")
        current_strategy_func(input_path, SUT_path, seed, bugs_logs_path)
        print(f"end of running {current_strategy_name}strategy")
        print()

    counter = 0
    print(f"running {generative_fuzzing_undefined_behaviour.STRATEGY_NAME} strategy")
    # create input directory
    sut_name = os.path.basename(os.path.normpath(SUT_path))
    pathlib.Path(os.path.join(input_path, sut_name, generative_fuzzing_undefined_behaviour.STRATEGY_NAME)).mkdir(
        parents=True, exist_ok=True)

    while True:
        full_input_file_path = os.path.join(input_path, sut_name, generative_fuzzing_undefined_behaviour.STRATEGY_NAME,
                                            f"{counter}.cnf")
        false_file_input_undefined_behaviour.run_strategy(full_input_file_path, SUT_path, seed, bugs_logs_path)
        generative_fuzzing_undefined_behaviour.run_strategy(full_input_file_path, SUT_path, seed, bugs_logs_path)
        counter += 1
