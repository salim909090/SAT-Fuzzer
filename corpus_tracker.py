import os
import subprocess as cmdlineprocess

"""Singleton Class to keep track of the coverage and store interesting 
inputs for further investigation"""
class Corpus:
    instance = None

    """Each item in the queue stores the input directory and a counter
    to represent a counter the number of mutations left for each input.
    Separate queues for both functional and undefined behaviour strategies."""
    interesting_cnfs_queue_ub = []
    interesting_cnfs_queue_fb = []

    current_coverage = 0

    def __init__(self):
        """ Virtually private constructor. """
        if Corpus.instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Corpus.instance = self

    """Return the static object"""
    @staticmethod
    def get_instance():
        """ Static access method. """
        if Corpus.instance is None:
            print("[+] New corpus")
            Corpus()

        return Corpus.instance

    """Check if the new input improved the coverage of the directory"""
    def compare_current_coverage(self, new_coverage, new_input, mode, tries):
        if new_coverage > self.current_coverage:
            self.current_coverage = new_coverage
            self.add_cnf(new_input, mode, tries)
        else:
            print("not interesting")

    """Add the cnf input to the corpus"""
    def add_cnf(self, new_input, mode, tries):
        print("Found interesting input")
        print("Adding to queue: "+"("+str(tries)+")"+new_input)
        if mode == "ub":
            self.interesting_cnfs_queue_ub.append([new_input, tries])
        else:
            print("not ub")

    """
    def find_coverage(self, path, new_input, mode, tries):
        command = "cd " + path + " \n gcovr"
        subprocess = cmdlineprocess.Popen(command, shell=True, stdout=cmdlineprocess.PIPE)
        subprocess_return = subprocess.stdout.read()
        subprocess_return = subprocess_return.splitlines()
        subprocess_return = subprocess_return[-2].decode("utf-8").split(" ")
        final_percentage = subprocess_return[-1].strip("%")

        if final_percentage == "--":
            final_percentage = 0
        else:
            final_percentage = int(final_percentage)
        print(final_percentage)

        self.compare_current_coverage(final_percentage, new_input, mode, tries)
        return final_percentage
    """

    """Find the coverage of the given directory"""
    def find_coverage(self, path, new_input, mode, tries):
        # Process the shell command and read the output
        command = "gcov -n " +path+"/*.c"
        subprocess = cmdlineprocess.Popen(command, shell=True, stdout=cmdlineprocess.PIPE)
        subprocess_return = subprocess.stdout.read()
        subprocess_return = subprocess_return.splitlines()

        # Calculate the total coverage of the directory for all the c files
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
        self.compare_current_coverage(final_percentage, new_input, mode, tries)

        print("Final Coverage: "+str(final_percentage))
        return final_percentage

    """Initialise inputs in to the queue given a directory path"""
    def initialise_queue(self, input_path, mode, tries):
        for current_input_filename in os.listdir(input_path):
            file_name_full_path = os.path.abspath(os.path.join(input_path, current_input_filename))
            # Append input to the right queue
            if mode == "ub":
                self.interesting_cnfs_queue_ub.append([file_name_full_path, tries])
            elif mode == "fb":
                self.interesting_cnfs_queue_fb.append([file_name_full_path, tries])

    """Check if a queue is empty for a given mode"""
    def queue_is_empty(self, mode):
        if mode == "ub":
            if len(self.interesting_cnfs_queue_ub) > 0:
                return False
            else:
                return True
        elif mode == "fb":
            if len(self.interesting_cnfs_queue_fb) > 0:
                return False
            else:
                return True

    """Pop items in a queue if the counter for a specific input hits 0"""
    def pop_queue(self, mode):
        if mode == "ub":
            if self.interesting_cnfs_queue_ub[0][1] > 0:
                print("Getting item from queue: "+"("+str(self.interesting_cnfs_queue_ub[0][1])+")"+self.interesting_cnfs_queue_ub[0][0])
                self.interesting_cnfs_queue_ub[0][1] = self.interesting_cnfs_queue_ub[0][1] - 1
                print(self.interesting_cnfs_queue_ub)
                return self.interesting_cnfs_queue_ub[0][0]
            else:
                print("Getting last item from queue: "+"("+str(self.interesting_cnfs_queue_ub[0][1])+")"+self.interesting_cnfs_queue_ub[0][0])
                last_item = self.interesting_cnfs_queue_ub.pop(0)
                print(self.interesting_cnfs_queue_ub)
                return last_item[0]
        elif mode == "fb":
            if self.interesting_cnfs_queue_fb[0][1] > 0:
                self.interesting_cnfs_queue_fb[0][1] = self.interesting_cnfs_queue_fb[0][1] - 1
                return self.interesting_cnfs_queue_fb[0][0]
            else:
                return self.interesting_cnfs_queue_fb.pop()[0]
