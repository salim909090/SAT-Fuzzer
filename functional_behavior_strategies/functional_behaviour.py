"""
The file contains the functions responsible to run the strategies
to detect wrong functional behaviour
"""
from functional_behavior_strategies import check_basic_functional_behaviour

# Dict of strategies to be run
strategies = {
    check_basic_functional_behaviour.STRATEGY_NAME: check_basic_functional_behaviour.run_strategy
}


def run_stategies(input_path, SUT_path, seed, bugs_logs_path):
    for current_strategy_name, current_strategy_func in strategies.items():
        print(f"running {current_strategy_name} strategy")
        current_strategy_func(input_path, SUT_path, seed, bugs_logs_path)
        print(f"end of running {current_strategy_name}strategy")
        print()
