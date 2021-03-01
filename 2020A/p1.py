import os
import sys


environment = 'pub'


def SetUpProblems(solver, parameter, logger=None, line_indicator=0):
    template = "Case #{0}: {1}"
    logger = SoftWrapper(logger)

    numTest = int(input())
    logger.print("The number is instances is "+str(numTest))

    for i in range(numTest):
        if parameter:  # for each test, there is a first line that define some hyper parameters
            hyper = list(map(int, input().split()))
            logger.print("Get hypper parameter " +
                         str(hyper)+" for Case "+str(i))
            result = solver(1, hyper)  # NEED CHANGE
            print(template.format(i+1, result))
        else:  # in this case, we assume there is only one line for each test case
            logger.print("Directly solve case "+str(i)+" assume line 1")
            result = solver(1)  # NEED CHANGE
            print(template.format(i+1, result))


def Solver(numLine, hyper=[]):
    data = {}
    for i in range(numLine):
        data[i] = list(map(int, input().split()))
    return Engine(data, hyper)


def Engine(data, hyper=[]):
    data = data[0]
    data=[item for item in data if item<=hyper[1]]
    #data.sort()
    data=countsort(data,0,hyper[1])
    total = 0
    times = 0
    for num in data:
        total += num
        if total > hyper[1]:
            return times
        else:
            times=times+1
    return times
import itertools

def countsort(data,min_val=None,max_val=None):
    if min_val is None:
        min_val=min(data)
    if max_val is None:
        max_val=max(data)
    #data=[item for item in data if item>=min_val]
    #data=[item for item in data if item<=max_val]
    index=[0]*(max_val-min_val+1)
    for item in data:
        index[item-min_val]+=1
    index=list(itertools.accumulate(index))
    result=[]
    prev=0
    for i,item in enumerate(index):
        result=result+([min_val+i]*(item-prev))
        prev=item
    return result

#######################################################################
import time
import os

default_loc='~/Documents/tmp'


class Logger:
    def __init__(self,loc=default_loc):
        if(loc[-1]!='/'):
            loc=loc+'/'

        # check if directory exists
        if not os.path.isdir(loc):
            result=create_dic(loc)
            if result<0:
                raise LoggerException("Failed to create dic "+loc)

        self.filename=loc+'log_'+time.asctime()+'.txt'
    
        self.level_dic=level_dic={0:"log",1:"warning",2:"warning handling",
                    3:"error",4:"error-handling",5:"log system warning"}

        
        self.f=open(self.filename,'w')
    
    def print(self,msg,level=0):
        if(not level in self.level_dic):
            msg="Trying to log message \""+msg+"\" with invalid level "+str(level)
            level=len(self.level_dic)-1
        if msg[-1]=='\n':
            msg=msg[0:-1]
        template="<<{0}>>[{1}] - {2}\n"
        self.f.write(template.format(time.asctime(),self.level_dic[level],msg))
        self.f.flush()

    def level_dic_lookup(self,level):
        if(not level in self.level_dic):
            return "Not Found"
        else:
            return self.level_dic[level]

    def __del__(self):
        self.f.close()

def create_dic(path):
    try:
        os.makedirs(path)
        return 0
    except Exception as e:
        print("A Exception is Thrown "+e)
        return -1

class LoggerException(Exception):
    def __init__(self, message):
        self.message=message

def SoftWrapper(var):
    if not var is None:
        return var
    else:
        return _SoftBlow()

class _SoftBlow:

    def __getattr__(self,name):
        return lambda *args:None

if __name__ == "__main__":
    if environment == 'dev':
        logger =Logger(os.getcwd()+'/tmp')
    else:
        logger = None
    parameter = True
    solver = Solver
    SetUpProblems(solver, parameter, logger)


