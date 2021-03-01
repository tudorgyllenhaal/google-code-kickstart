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

########################################################################
import os
import sys


environment = 'pub'
logger=None

if environment == 'dev':
    logger =Logger(os.getcwd()+'/tmp')
logger = SoftWrapper(logger)

def SetUpProblems(solver, parameter, line_indicator=0):
    template = "Case #{0}: {1}"

    numTest = int(input())
    logger.print("The number is instances is "+str(numTest))

    for i in range(numTest):
        if parameter:  # for each test, there is a first line that define some hyper parameters
            hyper = list(map(int, input().split()))
            logger.print("Get hypper parameter " +
                         str(hyper)+" for Case "+str(i))
            result = solver(hyper[0], hyper)  # NEED CHANGE
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


import numpy as np

count=0

def Engine(data, hyper=[]):
    data_np=np.zeros((hyper[0],hyper[1]))
    for i in range(hyper[0]):
        data_np[i,:]=np.array(data[i])
    table=np.zeros((hyper[0],hyper[2]))
    for i in range(hyper[2]):
        for j in range(hyper[0]):
            if j==0:
                table[j,i]=np.sum(data_np[j,0:i+1])
            else:
                if i==0:
                    table[j,i]=max(table[j-1,i],data_np[j,0])
                else:
                    if i>hyper[1]:
                        withNewLine=table[j-1,i-1:max(-1,i-1-hyper[1]):-1]+np.cumsum(data_np[j,0:i])
                    else:
                        withNewLine=table[j-1,i-1::-1]+np.cumsum(data_np[j,0:i])
                    singleLine=np.sum(data_np[j,0:i+1])
                    table[j,i]=max(table[j-1,i],singleLine,np.amax(withNewLine))
    
    return int(table[-1,-1])
    
    



if __name__ == "__main__":
    parameter = True
    solver = Solver
    SetUpProblems(solver, parameter)


