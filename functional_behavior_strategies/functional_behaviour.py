"""
The file contains the functions responsible to run the strategies
to detect wrong functional behaviour
"""
import time
import os
import psutil

from functional_behavior_strategies import check_basic_functional_behaviour, check_SAT_variables

# Dict of strategies to be run
strategies = {
    check_basic_functional_behaviour.STRATEGY_NAME: check_basic_functional_behaviour.run_strategy,
    check_SAT_variables.STRATEGY_NAME: check_SAT_variables.run_strategy
}


def run_strategies(input_path, SUT_path, seed, bugs_logs_path, start):
    for current_strategy_name, current_strategy_func in strategies.items():
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

        print(f"-- Running {current_strategy_name} strategy")
        current_strategy_func(input_path, SUT_path, seed, bugs_logs_path)
        print(f"[!] End of running {current_strategy_name} strategy")
        print()
