from SerialSetup import *
from AL5Dsetup import *

# ports = serial_ports()
# print(ports)
# portname = input('Ports found listed above. Enter name of port for robot arm: ')
# ser = serial.Serial(
#     port=portname,
#     baudrate=9600
# )

# print(ser.isOpen())

LastJointArray = [1500,1500,1500,1500,1500,1500]

smoothingThreshold = 50
steps = 15
delay = 0.05

mateValuesNow, mateResponse = getMateValues()

while True:
    ndPosArray = [0 for i in range(6)]
    empty = [0 for i in range(6)]
    ndPosArray = np.vstack([ndPosArray,empty])
    
    checkpointPos = getCheckpointPos()
    checkpointOffset = [-0.006,-0.01,0.007]
    newMateValues = GetJointAngles(checkpointPos[0]+checkpointOffset[0],checkpointPos[1]+checkpointOffset[1],checkpointPos[2]+checkpointOffset[2],mateValuesNow[6])
    print(mateValuesNow[7],mateValuesNow[8])
    setMateValues(mateResponse,newMateValues[0],newMateValues[1],newMateValues[2],newMateValues[3],mateValuesNow[7],mateValuesNow[8])
    mateValuesNow, mateResponse = getMateValues()

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
        # for i in range(len(x)):
        #     if x[i] != 0:
        #         command = '#'+str(i)+' P'+str(x[i])+'\r'
        #         ser.write(command.encode())
        #         time.sleep(delay)
    LastJointArray = mateValuesNow[0:5]
    time.sleep(0.5)