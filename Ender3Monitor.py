from Octoprint import *
from OnshapePlus import *

while True:
    jobInfo = opJobInfo()
    printerInfo, temps = opInfo()
    # print(jobInfo['state'])
    # print(jobInfo['progress']['completion'])
    # print(printerInfo)

    printerStatus(temps[0],temps[1],jobInfo['progress']['completion'])
    time.sleep(15)