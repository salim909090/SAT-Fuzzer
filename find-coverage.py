import subprocess


# Go to directory and run gcov and obtain final percentage coverage
def find_coverage():
    subprocess = subprocess.Popen("gcovr", shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess.stdout.read()
    subprocess_return = subprocess_return.splitlines()
    subprocess_return = subprocess_return[-2].decode("utf-8").split(" ")
    print(subprocess_return[-1])