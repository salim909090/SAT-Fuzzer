"""
The file contains the functions responsible to run the strategies
to detect undefined behaviour
"""
import os
import pathlib
import corpus_tracker
import time
import psutil

from undefined_behaviour_strategies import undefined_behavior_mutation_feedback_fuzzing
from undefined_behaviour_strategies import false_file_input_undefined_behaviour
from undefined_behaviour_strategies import generative_fuzzing_undefined_behaviour

# array of strategies to be run
strategies = {
    undefined_behavior_mutation_feedback_fuzzing.STRATEGY_NAME: undefined_behavior_mutation_feedback_fuzzing.run_strategy,
}


def run_strategies(input_path, SUT_path, seed, bugs_logs_path, input_bugs):
    corpus = corpus_tracker.Corpus.get_instance()
    corpus.initialise_queue(input_path, "ub", 0)
    for current_strategy_name, current_strategy_func in strategies.items():
        print(f"-- Running {current_strategy_name} strategy")
        status = current_strategy_func(input_path, SUT_path, seed, bugs_logs_path,input_bugs)
        print(f"[+] End of running {current_strategy_name}  strategy, " + status)
        print()

    counter = 0
    print(f"-- Running {generative_fuzzing_undefined_behaviour.STRATEGY_NAME} strategy")
    # create input directory
    sut_name = os.path.basename(os.path.normpath(SUT_path))
    path = pathlib.Path(os.path.join(input_path, sut_name, generative_fuzzing_undefined_behaviour.STRATEGY_NAME))

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    bugs_counter = 0
    start = time.time()
    while True:

        # Get Physical and Logical CPU Count
        full_input_file_path = os.path.join(input_path, sut_name, generative_fuzzing_undefined_behaviour.STRATEGY_NAME,
                                            f"{counter}.cnf")
        bugs_counter += false_file_input_undefined_behaviour.run_strategy(full_input_file_path, SUT_path, seed, bugs_logs_path,input_bugs)
        bugs_counter += generative_fuzzing_undefined_behaviour.run_strategy(full_input_file_path, SUT_path, seed, bugs_logs_path,input_bugs)
        end = time.time()
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        statistics = {}

        # Get Physical and Logical CPU Count
        physical_and_logical_cpu_count = os.cpu_count()
        statistics['physical_and_logical_cpu_count'] = physical_and_logical_cpu_count
        cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]
        statistics['cpu_load'] = cpu_load
        print("Runtime: {:0>2}:{:05.2f}".format(int(minutes), seconds) + f", Memory: " + str(psutil.virtual_memory().percent)+f" Running input {counter}, " + f" Bugs found {bugs_counter}," + f" Current coverage: {corpus.current_coverage}",end='\r')
        counter += 1
