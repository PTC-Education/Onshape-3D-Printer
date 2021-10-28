from Octoprint import *
from OnshapePlus import *

while True:
    jobInfo = opJobInfo()
    printerInfo, temps = opInfo()
    print(jobInfo['state'])
    print(jobInfo['progress']['completion'])
    print(temps)
    try:
        completion = int(jobInfo['progress']['completion'])
    except:
        completion = "not started"

    printerStatus(temps[1],temps[3],temps[0],temps[2],jobInfo['state'],completion)
    time.sleep(5)