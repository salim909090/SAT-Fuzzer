"""
The file contains the functions responsible to run the strategies
to detect undefined behaviour
"""
import os
import pathlib
import corpus_tracker
import time
import psutil

from undefined_behaviour_strategies import simple_sanitizer_undefined_behaviour
from undefined_behaviour_strategies import false_file_input_undefined_behaviour
from undefined_behaviour_strategies import generative_fuzzing_undefined_behaviour

# array of strategies to be run
strategies = {
    simple_sanitizer_undefined_behaviour.STRATEGY_NAME: simple_sanitizer_undefined_behaviour.run_strategy,
    false_file_input_undefined_behaviour.STRATEGY_NAME: false_file_input_undefined_behaviour.run_strategy
}


def run_strategies(input_path, SUT_path, seed, bugs_logs_path, start):
    corpus = corpus_tracker.Corpus.get_instance()
    corpus.initialise_queue(input_path, "ub", 0)
    for current_strategy_name, current_strategy_func in strategies.items():
        print(f"-- Running {current_strategy_name} strategy")
        current_strategy_func(input_path, SUT_path, seed, bugs_logs_path)
        print(f"[+] End of running {current_strategy_name}  strategy")
        print()

    counter = 0
    print(f"-- Running {generative_fuzzing_undefined_behaviour.STRATEGY_NAME} strategy")
    # create input directory
    sut_name = os.path.basename(os.path.normpath(SUT_path))
    path = pathlib.Path(os.path.join(input_path, sut_name, generative_fuzzing_undefined_behaviour.STRATEGY_NAME))

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    while True:
        end = time.time()
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        statistics = {}

        # Get Physical and Logical CPU Count
        physical_and_logical_cpu_count = os.cpu_count()
        statistics['physical_and_logical_cpu_count'] = physical_and_logical_cpu_count
        cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]
        statistics['cpu_load'] = cpu_load

        print("Runtime: {:0>2}:{:05.2f}".format(int(minutes), seconds))
        # print(f"CPU: {cpufreq.current / 1000:.2f} GHz")
        print(f"Memory: " + str(psutil.virtual_memory().percent) + " %")
        print(f"CPU: {statistics['cpu_load']:.2f} % (" + str(physical_and_logical_cpu_count) + " cores)")
        print('Total Coverage Score: {:0.4f}%'.format(0))
        print('Possible Bugs found: {:d}'.format(0))

        full_input_file_path = os.path.join(input_path, sut_name, generative_fuzzing_undefined_behaviour.STRATEGY_NAME,
                                            f"{counter}.cnf")
        generative_fuzzing_undefined_behaviour.run_strategy(full_input_file_path, SUT_path, seed, bugs_logs_path)
        counter += 1
