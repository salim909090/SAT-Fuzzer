import subprocess as cmdlineprocess

command = "gcov -n " +"solvers/solver2/*.c"
subprocess = cmdlineprocess.Popen(command, shell=True, stdout=cmdlineprocess.PIPE)
subprocess_return = subprocess.stdout.read()
subprocess_return = subprocess_return.splitlines()

accum_covered = 0
accum_total = 0

for line in subprocess_return:
    line = line.decode("utf-8")
    if("Lines executed" in line):
        info = line.strip("Lines executed:")
        info_disect = info.split(" ")
        percentage_disect = info_disect[0]
        percentage_disect = percentage_disect.strip("%")

        accum_total = accum_total +int(info_disect[2])
        accum_covered = accum_covered + (float(percentage_disect)/100)*int(info_disect[2])
    
final_percentage = accum_covered/accum_total
print(final_percentage)


