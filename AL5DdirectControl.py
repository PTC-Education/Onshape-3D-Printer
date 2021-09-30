from Octoprint import opJog
from os import error
from SerialSetup import *
from AL5Dsetup import *

ports = serial_ports()
print(ports)
portname = input('Ports found listed above. Enter name of port for robot arm: ')
ser = serial.Serial(
    port=portname,
    baudrate=9600
)

print(ser.isOpen())

smoothingThreshold = 50
steps = 15
delay = 0.05

LastJointArray = [1500,1500,1500,1500,1500,1500]

for i in range(len(LastJointArray)):
                if LastJointArray[i] != 0:
                    command = '#'+str(i)+' P'+str(LastJointArray[i])+'\r'
                    ser.write(command.encode())
                    time.sleep(delay)

mateValuesNow, mateResponse = getMateValues()
lastEnder3YXZ = [mateValuesNow[9],mateValuesNow[10],mateValuesNow[11]]

try:
    while True:
        ndPosArray = [0 for i in range(6)]
        empty = [0 for i in range(6)]
        ndPosArray = np.vstack([ndPosArray,empty])
        
        checkpointPos = getCheckpointPos()
        checkpointOffset = [-0.006,-0.01,0.007]
        newMateValues = GetJointAngles(checkpointPos[0]+checkpointOffset[0],checkpointPos[1]+checkpointOffset[1],checkpointPos[2]+checkpointOffset[2],mateValuesNow[6])
        # print(mateValuesNow[7],mateValuesNow[8])
        setMateValues(mateResponse,newMateValues[0],newMateValues[1],newMateValues[2],newMateValues[3],mateValuesNow[7],mateValuesNow[8])
        mateValuesNow, mateResponse = getMateValues()
        newEnder3YXZ = [mateValuesNow[9],mateValuesNow[10],mateValuesNow[11]]
        # print(mateValuesNow)
        print(mateValuesNow[0:6])
        # print(LastJointArray)
        if lastEnder3YXZ != newEnder3YXZ:
            yjog = int((lastEnder3YXZ[0] - newEnder3YXZ[0])*1000)
            xjog = int((newEnder3YXZ[1] - lastEnder3YXZ[1])*1000)
            zjog = int((newEnder3YXZ[2] - lastEnder3YXZ[2])*1000)
            # print(xjog,yjog,zjog)
            opJog(xjog,yjog,zjog)

        for i in range(6):
            if LastJointArray[i] - mateValuesNow[i] < 0:
                posArray = np.array(range(LastJointArray[i],mateValuesNow[i],steps))
            else:
                posArray = np.array(range(LastJointArray[i],mateValuesNow[i],-steps))
            for j in range(len(posArray)):
                try:
                    ndPosArray[j][i] = posArray[j]
                except:
                    ndPosArray = np.vstack([ndPosArray,empty])
                    ndPosArray[j][i] = posArray[j]

        for x in ndPosArray:
            print(x)
            for i in range(len(x)):
                if x[i] != 0:
                    command = '#'+str(i)+' P'+str(x[i])+'\r'
                    ser.write(command.encode())
                    time.sleep(delay)
        LastJointArray = mateValuesNow[0:6]
        LastFullArray = mateValuesNow
        lastEnder3YXZ = [mateValuesNow[9],mateValuesNow[10],mateValuesNow[11]]
        time.sleep(0.5)
except KeyboardInterrupt:
    ser.close()
    pass
except:
    print(error)
    ser.close()