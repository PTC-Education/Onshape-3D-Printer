from Octoprint import *

jobInfo = opJobInfo()
printerInfo = opInfo()
print(jobInfo['state'])
print(jobInfo['progress']['completion'])
print(printerInfo)

opJog(0,5,0)