"""
Entry point of the SAT solver fuzzer

- Check the input args to the fuzzer
- Depending on the mode supplied it fuzzes all strategies in the mode

"""

import argparse
import os
# import subprocess
import corpus_tracker

from functional_behavior_strategies import functional_behaviour
from undefined_behaviour_strategies import undefined_behaviour

exec_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
args = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SAT fuzzer usage options")
    parser.add_argument('sut', type=str, help="Source directory of the SUT")
    parser.add_argument('inputs_path', type=str,
                        help="Directory containing a non-empty set of well-formed DIMACS-format files")
    parser.add_argument('--mode', help="Functional or Undefined behaviour mode")
    parser.add_argument('--seed', help="Path to the target sut to fuzz")
    args = parser.parse_args()

# Create output directory, remove and recreate
# output_dir = os.path.abspath(os.path.join(exec_dir, "fuzzed-tests"))
# subprocess.call(["rm", "-rf", output_dir], shell=False)
# subprocess.call(["mkdir", output_dir], shell=False)

# SUT path
sut_path = os.path.abspath(args.sut)

# Input directory
input_dir = os.path.abspath(args.inputs_path)

bugs_logs = "fuzzed-tests"

corpus = corpus_tracker.Corpus.get_instance()

if args.mode == "ub":
    print("[+] Running all strategies to detect undefined behaviour")
    undefined_behaviour.run_strategies(args.inputs_path, sut_path, args.seed, bugs_logs)
elif args.mode == "fb":
    print("[+] Running all strategies to detect functional behaviour")
    functional_behaviour.run_strategies(args.inputs_path, sut_path, args.seed, bugs_logs)
else:
    print("[+] Running all strategies to detect functional and undefined behaviour")
    undefined_behaviour.run_strategies(args.inputs_path, sut_path, args.seed, bugs_logs)
    functional_behaviour.run_strategies(args.inputs_path, sut_path, args.seed, bugs_logs)
