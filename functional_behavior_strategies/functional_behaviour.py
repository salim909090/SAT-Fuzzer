"""
The file contains the functions responsible to run the strategies
to detect wrong functional behaviour
"""
import time
import os
import psutil

from functional_behavior_strategies import check_basic_functional_behaviour

# Dict of strategies to be run
strategies = {
    check_basic_functional_behaviour.STRATEGY_NAME: check_basic_functional_behaviour.run_strategy,
}


def run_strategies(input_path, SUT_path, seed, bugs_logs_path,input_bugs):
    for current_strategy_name, current_strategy_func in strategies.items():
        print(f"-- Running {current_strategy_name} strategy")
        status = current_strategy_func(input_path, SUT_path, seed, bugs_logs_path,input_bugs)
        print(f"[!] End of running {current_strategy_name} strategy, " + status)
        print()
