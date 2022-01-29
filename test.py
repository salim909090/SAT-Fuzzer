import corpus_tracker
import subprocess as cmdlineprocess

tester = corpus_tracker.Corpus()
path = "solvers/solver2"


tester.find_coverage(path,"hey")

command = "python3 fuzz-sat.py solvers/solver2/ inputs/ --mode ub --seed 1234567"
subprocess = cmdlineprocess.Popen(command, shell=True, stdout=cmdlineprocess.PIPE)

tester.find_coverage(path,"BYE")
