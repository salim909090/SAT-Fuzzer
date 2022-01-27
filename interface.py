import time

from os import system


if __name__ == "__main__":

    start = time.time()
    start_time = time.clock_gettime(time.CLOCK_MONOTONIC)

    while 1:
        system('clear')
        current_time = time.clock_gettime(time.CLOCK_MONOTONIC)
        past_time = start_time
        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("FUZZING SAT SOLVER\n" + '-'*18)
        print("Stats\n")
        print("Runtime: {:0>2}:{:05.2f}".format(int(minutes),seconds))
        print('Total Coverage Score: {:0.4f}%'.format(0))
        print('Possible Bugs found: {:d}'.format(0))
        time.sleep(1)

