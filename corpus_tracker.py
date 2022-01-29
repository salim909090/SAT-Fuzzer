import subprocess as cmdlineprocess
import os

class Corpus:
    instance = None

    interesting_cnfs_queue_ub = []
    interesting_cnfs_queue_fb = []
    current_coverage = 0

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Corpus.instance == None:
            print("new corpus")
            Corpus()
        return Corpus.instance
        
    def __init__(self):
        """ Virtually private constructor. """
        if Corpus.instance != None:
            raise Exception("This class is a singleton!")
        else:
            Corpus.instance = self

    def compare_current_coverage(self,new_coverage,new_input,mode,tries):
        if(new_coverage>self.current_coverage):
            self.current_coverage = new_coverage
            self.add_cnf(new_input,mode,tries)
        else:
            print("not interesting")

    def add_cnf(self,new_input,mode,tries):
        print("Found interesting input")
        if(mode=="ub"):
            self.interesting_cnfs_queue_ub.append([new_input,tries])

    def find_coverage(self,path,new_input,mode,tries):
        command = "cd "+path+" \n gcovr"
        subprocess = cmdlineprocess.Popen(command, shell=True, stdout=cmdlineprocess.PIPE)
        subprocess_return = subprocess.stdout.read()
        subprocess_return = subprocess_return.splitlines()
        subprocess_return = subprocess_return[-2].decode("utf-8").split(" ")
        final_percentage = subprocess_return[-1].strip("%")

        if final_percentage=="--":
            final_percentage = 0
        else:
            final_percentage = int(final_percentage)
        print(final_percentage)

        self.compare_current_coverage(final_percentage,new_input,mode,tries)
        return final_percentage

    def initialise_queue(self,input_path,mode,tries):
        for current_input_filename in os.listdir(input_path):
            file_name_full_path = os.path.abspath(os.path.join(input_path,current_input_filename))
            if(mode == "ub"):
                self.interesting_cnfs_queue_ub.append([file_name_full_path,tries])
    
    def queue_is_empty(self,mode):
        if mode == "ub":
            if len(self.interesting_cnfs_queue_ub) >0:
                return False
            else:
                return True
        elif mode == "fb":
            if len(self.interesting_cnfs_queue_fb) >0:
                return False
            else:
                return True

    def pop_queue(self,mode):
        if mode == "ub":
            if self.interesting_cnfs_queue_ub[0][1] > 0:
                print("test")
                self.interesting_cnfs_queue_ub[0][1] = self.interesting_cnfs_queue_ub[0][1] -1
                return self.interesting_cnfs_queue_ub[0][0]
            else:
                return self.interesting_cnfs_queue_ub.pop()[0]
        elif mode == "fb":
            if self.interesting_cnfs_queue_fb[0][1] > 0:
                self.interesting_cnfs_queue_fb[0][1] = self.interesting_cnfs_queue_fb[0][1] -1
                return self.interesting_cnfs_queue_fb[0][0]
            else:
                return self.interesting_cnfs_queue_fb.pop()[0]

