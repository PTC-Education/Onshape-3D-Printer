from OnshapePlus import *
import math
import numpy as np

url = 'https://cad.onshape.com/documents/f5405092df38df2bb9ff1a24/w/802789005337ddbf1908553c/e/96ccba7ab79a0fcb270c067a'

##
##
## Onshape Functions for robot arm assembly
##
##
def getMateValues():
    RobotData = []
    RobotData = [0 for i in range(12)]
    fixed_url = '/api/assemblies/d/did/w/wid/e/eid/matevalues'

    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v2+json',
            'Content-Type': 'application/vnd.onshape.v2+json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    fullResponse = json.loads(response.data)
    # print(json.dumps(fullResponse, indent=4, sort_keys=True))

    for i in range(len(fullResponse["mateValues"])):
        if fullResponse['mateValues'][i]['mateName'] == "Base":
            RobotData[0] = int(translate(fullResponse['mateValues'][i]['rotationZ'],0,3.14,500,2500))
        elif fullResponse['mateValues'][i]['mateName'] == "Shoulder":
            RobotData[1] = int(translate(fullResponse['mateValues'][i]['rotationZ'],0,3.14,500,2500))
        elif fullResponse['mateValues'][i]['mateName'] == "Elbow":
            RobotData[2] = int(translate(fullResponse['mateValues'][i]['rotationZ'],0,3.14,500,2500))-70
        elif fullResponse['mateValues'][i]['mateName'] == "Wrist":
            if fullResponse['mateValues'][i]['rotationZ'] > 3.14:
                fullResponse['mateValues'][i]['rotationZ'] = fullResponse['mateValues'][i]['rotationZ'] - 3.14
            elif fullResponse['mateValues'][i]['rotationZ'] < 0:
                fullResponse['mateValues'][i]['rotationZ'] = fullResponse['mateValues'][i]['rotationZ'] + 3.14
            RobotData[3] = int(translate(fullResponse['mateValues'][i]['rotationZ'],0,3.14,2500,500))+50
        elif fullResponse['mateValues'][i]['mateName'] == "Hand":
            RobotData[4] = int(translate(fullResponse['mateValues'][i]['rotationZ'],-math.pi/2,math.pi/2,500,2500))
        elif fullResponse['mateValues'][i]['mateName'] == "Gripper":
            RobotData[5] = int(translate(fullResponse['mateValues'][i]['rotationZ'],0,3.14,500,2500))
        elif fullResponse['mateValues'][i]['mateName'] == "Gripper Angle":
            RobotData[6] = int(translate(fullResponse['mateValues'][i]['translationZ'],0,0.127,90,0))
        elif fullResponse['mateValues'][i]['mateName'] == "Gripper Rotation":
            RobotData[7] = translate(fullResponse['mateValues'][i]['translationZ'],0,0.127,math.pi/2,-math.pi/2)
        elif fullResponse['mateValues'][i]['mateName'] == "Open Close":
            RobotData[8] = translate(fullResponse['mateValues'][i]['translationZ'],0,0.127,0,math.pi)
        elif fullResponse['mateValues'][i]['mateName'] == "Y Axis":
            RobotData[9] = fullResponse['mateValues'][i]['translationZ']
        elif fullResponse['mateValues'][i]['mateName'] == "X Axis":
            RobotData[10] = fullResponse['mateValues'][i]['translationZ']
        elif fullResponse['mateValues'][i]['mateName'] == "Z Axis":
            RobotData[11] = fullResponse['mateValues'][i]['translationZ']

    return RobotData, fullResponse

def getCheckpointPos():
    fixed_url = '/api/assemblies/d/did/w/wid/e/eid'

    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
            'Content-Type': 'application/json'}
    method = 'GET'

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    parsed = json.loads(response.data)

    for i in range(len(parsed['rootAssembly']['instances'])):
        if "Checkpoint" in parsed['rootAssembly']['instances'][i]['name']:
            checkpointId = parsed['rootAssembly']['instances'][i]['id']
            break
    
    for i in range(len(parsed['rootAssembly']['occurrences'])):
        if parsed['rootAssembly']['occurrences'][i]['path'][0] == checkpointId and len(parsed['rootAssembly']['occurrences'][i]['path'])==1:
            checkpointPos = [parsed['rootAssembly']['occurrences'][i]['transform'][3],parsed['rootAssembly']['occurrences'][i]['transform'][7],parsed['rootAssembly']['occurrences'][i]['transform'][11]]
            break

    return checkpointPos

def setMateValues(fullResponse,baseAngle,shoulderAngle,elbowAngle,wristAngle,handAngle,gripperAngle):
    fixed_url = '/api/assemblies/d/did/w/wid/e/eid/matevalues'

    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    # method = 'GET'

    # params = {}
    # payload = {}
    # headers = {'Accept': 'application/vnd.onshape.v2+json',
    #         'Content-Type': 'application/vnd.onshape.v2+json'}

    # response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    # fullResponse = json.loads(response.data)
    newPayload = {'mateValues':[]}

    for i in range(len(fullResponse["mateValues"])):
        if fullResponse['mateValues'][i]['mateName'] == "Base":
            fullResponse['mateValues'][i]['rotationZ'] = baseAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])

    method = 'POST'

    params = {}
    payload = newPayload
    headers = {'Accept': 'application/vnd.onshape.v2+json',
            'Content-Type': 'application/vnd.onshape.v2+json'}
    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    newPayload = {'mateValues':[]}
    for i in range(len(fullResponse["mateValues"])):
        if fullResponse['mateValues'][i]['mateName'] == "Base":
            fullResponse['mateValues'][i]['rotationZ'] = baseAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])
        elif fullResponse['mateValues'][i]['mateName'] == "Shoulder":
            fullResponse['mateValues'][i]['rotationZ'] = shoulderAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])
        elif fullResponse['mateValues'][i]['mateName'] == "Elbow":
            fullResponse['mateValues'][i]['rotationZ'] = elbowAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])
        elif fullResponse['mateValues'][i]['mateName'] == "Wrist":
            fullResponse['mateValues'][i]['rotationZ'] = wristAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])
        elif fullResponse['mateValues'][i]['mateName'] == "Hand":
            fullResponse['mateValues'][i]['rotationZ'] = handAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])
        elif fullResponse['mateValues'][i]['mateName'] == "Gripper":
            fullResponse['mateValues'][i]['rotationZ'] = gripperAngle
            newPayload['mateValues'].append(fullResponse['mateValues'][i])
        

    method = 'POST'

    params = {}
    payload = newPayload
    headers = {'Accept': 'application/vnd.onshape.v2+json',
            'Content-Type': 'application/vnd.onshape.v2+json'}
    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    # The command below prints the entire JSON response from Onshape
    print(response.status)


##
##
## Inverse Kinematics for Robot Arm
##
##
DegToRad = math.pi/180
RadToDeg = 180/math.pi

FloorToFirstJoint = 2.61*0.0254
UpperArmLength = 5.74*0.0254
ForeArmLength = 7.23*0.0254
GripperLength = 4.43*0.0254

def GetJointAngles(TCPx,TCPy,TCPz,WristAngleIn):
    BaseAngle = math.atan2(TCPx,TCPy)

    TCPq = math.sqrt(TCPx**2 + TCPy**2)
    TCPp = TCPz - FloorToFirstJoint

    WristQ = TCPq - GripperLength*math.cos(WristAngleIn*DegToRad)
    WristP = TCPp + GripperLength*math.sin(WristAngleIn*DegToRad)

    D2 = math.sqrt(WristP**2 + WristQ**2)
    # print(WristQ,WristP)

    ElbowAngle = math.acos((WristP**2 + WristQ**2 - UpperArmLength**2 - ForeArmLength**2)/(2*UpperArmLength*ForeArmLength))

    a1 = math.atan2(ForeArmLength*math.sin(ElbowAngle),UpperArmLength + ForeArmLength*math.cos(ElbowAngle))
    a2 = math.atan2(WristP,WristQ)
    ShoulderAngle = a1 + a2

    WristAngleOut = ShoulderAngle - ElbowAngle + WristAngleIn*DegToRad + math.pi/2

    # print(numpy.dot([BaseAngle, ShoulderAngle, ElbowAngle, WristAngleOut],RadToDeg))
    return [BaseAngle, ShoulderAngle, ElbowAngle, WristAngleOut]

