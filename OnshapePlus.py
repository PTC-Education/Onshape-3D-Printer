from os import access
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
## Onshape Functions
##
##

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

def printerStatus(nozzleTemp,bedTemp,printStatus):
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
    print(json.loads(response.data)["features"][2]["message"]["entities"][0]["message"]['parameters'][1]['message']['value'])

    newText = 'Nozzle Temp: '+str(nozzleTemp)+'''
Bed Temp: '''+str(bedTemp)+'''
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