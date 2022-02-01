import os
import time
import psutil

if __name__ == "__main__":

    start = time.time()

    while 1:
        # os.system('clear')
        print()

        end = time.time()
        hours, rem = divmod(end-start, 3600)
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
        time.sleep(1)



