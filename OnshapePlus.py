from os import access
from Octoprint import *
import time
import math
import serial
import sys
import glob
import json
import array

##
##
## Import and configure Onshpae Client
##
##
print('importing Onshape Client...')
from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement
print('configuring Onshape Client...')
try:
    try:
        try:
            exec(open('../apikeys.py').read())
            base = 'https://cad.onshape.com'
            client = Client(configuration={"base_url": base,
                                        "access_key": access,
                                        "secret_key": secret})
            print('client configured')
        except:
            exec(open('../../apikeys.py').read())
            base = 'https://cad.onshape.com'
            client = Client(configuration={"base_url": base,
                                        "access_key": access,
                                        "secret_key": secret})
            print('client configured')
    except:
        exec(open('apikeys.py').read())
        base = 'https://cad.onshape.com'
        client = Client(configuration={"base_url": base,
                                    "access_key": access,
                                    "secret_key": secret})
        print('client configured')
except:
    print('Api keys file not found. Input keys manually.')
    access = input('Please enter your access key: ')
    secret = input('Please enter your secret key: ')
    base = 'https://cad.onshape.com'
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('client configured')

##
##
## Utility Functions
##
##
def exportSliceUpload(url: str, config: str, filename: str, printerConfig: str):
    exportSTL(url,filename,config)
    gcodefile = filename.replace(".stl",".gcode")
    try:
        command = "slic3r-prusa3d --no-gui --load "+printerConfig+" "+filename
        # Suppress the output in order to not break the EMSSS
        suppress = " >/dev/null 2>&1"

        # Run the gcode generation and 
        os.system(command + suppress)
        s=""
        with open(gcodefile) as f: s = f.read()
        
        uploadFileToOctoprint(gcodefile, s)
        opStartPrint(gcodefile)
    except:
        print('fail')

##
##
## Basic Onshape Functions
##
##

## Get list of elements in document
def documentElementsList(url: str):
  fixed_url = '/api/documents/d/did/w/wid/elements'
  element = OnshapeElement(url)
  fixed_url = fixed_url.replace('did', element.did)
  fixed_url = fixed_url.replace('wid', element.wvmid)
  method = 'GET'

  params = {}
  payload = {}
  headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

  response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

  parsed = json.loads(response.data)
  # The command below prints the entire JSON response from Onshape
  # print(json.dumps(parsed, indent=4, sort_keys=True))
  return parsed

## Add initial appelement for printer monitor and control
def addAppElement(url:str,name="Octoprint AppElement"):
    fixed_url = '/api/appelements/d/did/w/wid'
    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)

    method = 'POST'

    params = {}
    payload = {
        "formatId": "com.python",
        "name": name,
        "description": "Created App Element",
        "jsonTree": {
            "printerInfo":{},
            "jobInfo":{},
            "image":"pending",
            "printQueue":[],
            "printerCommand":"none",
            "updateInfo":""
        }
    }
    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}
    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    return parsed

## Get app element JSON tree
def getJsonTree(url:str):
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content/json'
    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v2+json',
            'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)

    return parsed

## Add a key to the JSON Tree of the app element
def addAppElementJsonKey(url:str,newKeyName="foo",newKeyValue="bar"):
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content'
    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'POST'

    # Insertion: { 'btType' : 'BTJEditInsert-2523', 'path' : path, 'value' : newValue }

    params = {}
    payload = {
        "parentChangeId": getJsonTree(url)['changeId'],
        "jsonTreeEdit": {'btType' : 'BTJEditInsert-2523', 
                        'path' : { 'btType' : 'BTJPath-3073', 'startNode' : '', 'path' : [{ 'btType' : 'BTJPathKey-3221', 'key' : newKeyName }] }, 
                        'value' : newKeyValue }
        }

    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    return parsed

## Update the value of a key from the JSON tree
def updateAppElementJsonKey(url:str,keyName="foo",keyValue="bar"):
    fixed_url = '/api/appelements/d/did/w/wid/e/eid/content'
    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'POST'

    params = {}
    payload = {
        "parentChangeId": getJsonTree(url)['changeId'],
        "jsonTreeEdit": {'btType' : "BTJEditChange-2636", 
                        'path' : { 'btType' : 'BTJPath-3073', 'startNode' : '', 'path' : [{ 'btType' : 'BTJPathKey-3221', 'key' : keyName }] }, 
                        'value' : keyValue }
        }

    headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    return parsed

## Get Mates Function
def getMates(url):
    fixed_url = '/api/assemblies/d/did/w/wid/e/eid/matevalues'
    element = OnshapeElement(url)
    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v2+json',
                'Content-Type': 'application/vnd.onshape.v2+json'}

    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    return parsed

def setMates(url,body):
    fixed_url = '/api/assemblies/d/did/w/wid/e/eid/matevalues'
    element = OnshapeElement(url)
    method = 'POST'

    params = {}
    payload = body
    headers = {'Accept': 'application/vnd.onshape.v2+json',
                'Content-Type': 'application/vnd.onshape.v2+json'}

    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    return parsed

## Mass Prop test
def massProp(url: str):
  fixed_url = '/api/partstudios/d/did/w/wid/e/eid/massproperties'
  element = OnshapeElement(url)
  method = 'GET'

  params = {}
  payload = {}
  headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
            'Content-Type': 'application/json'}

  fixed_url = fixed_url.replace('did', element.did)
  fixed_url = fixed_url.replace('wid', element.wvmid)
  fixed_url = fixed_url.replace('eid', element.eid)

  response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
  print(response.status)
  print(response.data)
  parsed = json.loads(response.data)
  # The command below prints the entire JSON response from Onshape
  print(json.dumps(parsed, indent=4, sort_keys=True))
  return parsed

## Basic Documents test
def documents(params = {}):
  fixed_url = '/api/documents'
  method = 'GET'

  payload = {}
  headers = {'Accept': 'application/vnd.onshape.v1+json',
            'Content-Type': 'application/json'}

  response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

  # parsed = json.loads(response.data)
  # The command below prints the entire JSON response from Onshape
  # print(json.dumps(parsed, indent=4, sort_keys=True))
  return response.status

## Export STL from Part Studio
def exportSTL(url: str, filename="OnshapePart.stl", configuration=""):
    fixed_url = '/api/partstudios/d/did/w/wid/e/eid/stl'
    element = OnshapeElement(url)
    method = 'GET'

    params = {"units":"millimeter",
    "configuration":configuration}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+octet-stream',
            'Content-Type': 'application/json'}

    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    with open(filename, 'wb') as f:
        f.write(response.data.encode())
    print('file exported as '+filename)

## Get configuration from element
def getElementConfiguration(url: str):
    fixed_url = '/api/elements/d/did/w/wid/e/eid/configuration'
    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
            'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    parsed = json.loads(response.data)
    # The command below prints the entire JSON response from Onshape
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    return parsed

def getPartsInPartStudio(url: str):
    fixed_url = '/api/parts/d/did/w/wid/e/eid/'

    element = OnshapeElement(url)
    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
                'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

    parsed = json.loads(response.data)
    return parsed

def printerStatus(nozzleTemp,nozzleTarget,bedTemp,bedTarget,printerState,printStatus):
    fixed_url = '/api/partstudios/d/did/w/wid/e/eid/features'

    element = OnshapeElement('https://cad.onshape.com/documents/f5405092df38df2bb9ff1a24/w/802789005337ddbf1908553c/e/18dfb6003d165ccc97db128c')

    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid)

    method = 'GET'
    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
            'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    # print(json.loads(response.data)["features"][2]["message"]["entities"][0]["message"]['parameters'][1]['message']['value'])

    newText = 'Nozzle Temp: '+str(int(nozzleTemp))+''' deg C
Nozzle Target: '''+str(int(nozzleTarget))+''' deg C
Bed Temp: '''+str(int(bedTemp))+''' deg C
Bed Target: '''+str(int(bedTarget))+''' deg C
Printer State: '''+printerState+'''
Percent Complete: '''+str(printStatus)+'%'

    newFeature = json.loads(response.data)["features"][2]
    newFeature["message"]["entities"][0]["message"]['parameters'][1]['message']['value'] = newText
    # print(newFeature["message"]["entities"][0]["message"]['parameters'][1]['message']['value'])
    # print(timeRemaining)
    # print(json.loads(response.data)["sourceMicroversion"])
    # print(json.loads(response.data)["serializationVersion"])

    fixed_url = '/api/partstudios/d/did/w/wid/e/eid/features/featureid/fid'

    fid = json.loads(response.data)["features"][2]["message"]["featureId"]

    fixed_url = fixed_url.replace('did', element.did)
    fixed_url = fixed_url.replace('wid', element.wvmid)
    fixed_url = fixed_url.replace('eid', element.eid, 1)
    fixed_url = fixed_url.replace('fid', fid)

    # print(fixed_url)

    method = 'POST'
    params = {}
    payload = {'feature': newFeature,
            'serializationVersion': json.loads(response.data)["serializationVersion"],
            'sourceMicroversion': json.loads(response.data)["sourceMicroversion"]}
    headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
            'Content-Type': 'application/json'}

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)
    # print(response.data)

##
##
## Helper Functions
##
##
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)