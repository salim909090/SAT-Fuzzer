'''
entry point of the fuzzer
-check the input args to the fuzzer
-depending on the mode supplied it fuzzes all strategies in the mode
'''
import sys 
from functional_behavior_strategies import functional_behaviour
from undefined_behaviour_strategies import undefined_behaviour

input_path = sys.argv[1]
sut_path =  sys.argv[2]
seed =  sys.argv[3]
mode = sys.argv[4]
bugs_logs = "fuzzed-tests"

if mode == "ub":
    print("running all stratgies to detect undefined behviour")
    undefined_behaviour.run_stragies(input_path,sut_path,seed,bugs_logs)
elif mode == "fb":
    print("running all stratgies to detect functional behviour")
    functional_behaviour.run_stargies(input_path,sut_path,seed,bugs_logs)
else:
    print("running all stratgies to detect functional and undefined behviour")
    undefined_behaviour.run_stragies(input_path,sut_path,seed,bugs_logs)
    functional_behaviour.run_stargies(input_path,sut_path,seed,bugs_logs)
