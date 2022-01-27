import argparse
import os
import subprocess

exec_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SAT fuzzer interface")
    parser.add_argument('sut', help="refers to the source directory of the SUT")
    parser.add_argument('inputs', help="refers to a directory containing a non-empty set of well-formed DIMACS-format files")
    parser.add_argument('--seed', help="the path to the target sut to fuzz")
    args = parser.parse_args()

# Create output directory, remove and recreate
output_dir = os.path.abspath(os.path.join(exec_dir, "fuzzed-tests"))
subprocess.call(["rm", "-rf", output_dir], shell=False)
subprocess.call(["mkdir", output_dir], shell=False)

# SUT path
sut_path = os.path.abspath(args.sut)

# Input directory
input_dir = os.path.abspath(args.inputs)