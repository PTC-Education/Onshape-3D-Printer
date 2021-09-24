import requests
import json
import time
import os
import sys
import binascii

##
##
## Define base URL of octoprint server
##
##
base = "http://octopi.local"

##
##
## Import api key
##
##
print('Looking for apikeys.py file...')

try:
    try:
        exec(open('../apikeys.py').read())
        print('api key named OPapiKey found')
    except:
        exec(open('apikeys.py').read())
        print('api key named OPapiKey found')
except:
    print('Api keys file not found. Input key manually.')
    OPapiKey = input('Please enter your api key: ')

def connect():
    url = "/api/connection"

    payload={"command": "connect",
            "autoconnect": True}
    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }
    params = {}

    response = requests.request("POST", base+url, params=params, headers=headers, data=json.dumps(payload))
    print(response)

def opInfo():
    url = "/api/printer"

    payload="{}"
    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }
    params = {}
    params = {'history':'false'}

    response = requests.request("GET", base+url, params=params, headers=headers, data=payload)
    # print(response)
    FullResponse = json.dumps(response.json(), indent=4, sort_keys=True)
    # print(FullResponse)
    BedTemp = response.json()['temperature']['bed']['actual']
    ToolTemp = response.json()['temperature']['tool0']['actual']
    BedTempTarget = response.json()['temperature']['bed']['target']
    ToolTempTarget = response.json()['temperature']['tool0']['target']

    return response, [BedTemp,ToolTemp,BedTempTarget,ToolTempTarget]

def opJobInfo():
    url = "/api/job"

    payload="{}"
    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }
    params = {}
    params = {'history':'false'}

    response = requests.request("GET", base+url, params=params, headers=headers, data=payload)
    # print(response)
    FullResponse = json.dumps(response.json(), indent=4, sort_keys=True)
    # print(FullResponse)
    return response

def opHome():
    url = "/api/printer/printhead"

    payload={
        "command":"home",
        "axes": ["x", "y","z"]
    }
    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }

    response = requests.request("POST", base+url, headers=headers, data=json.dumps(payload))
    print(response)


def opJog(x,y,z):
    url = "/api/printer/printhead"

    payload={
        "command":"jog",
        "x": x,
        "y": y,
        "z": z
    }
    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }

    response = requests.request("POST", base+url, headers=headers, data=json.dumps(payload))
    try:
        FullResponse = json.dumps(response.json(), indent=4, sort_keys=True)
    except:
        print(response)

def opStartPrint(filename):
    url = "/api/files/local/"+filename

    payload={
    "command": "select",
    "print": True
    }

    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }

    response = requests.request("POST", base+url, headers=headers, data=json.dumps(payload))
    try:
        FullResponse = json.dumps(response.json(), indent=4, sort_keys=True)
        print(FullResponse)
    except:
        print(response)

def opStop():
    base = "http://octopi.local"
    url = "/api/job"

    payload = {
    "command": "cancel"
    }

    headers = {
    'X-Api-Key': OPappKey,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }

    response = requests.request("POST", base+url, headers=headers, data=json.dumps(payload))
    try:
        FullResponse = json.dumps(response.json(), indent=4, sort_keys=True)
    except:
        print(response)
        print(FullResponse)

'''
uploadFileToOctoprint():
    Inputs:
        
        fileName: name of the file stored locally, or response object
                  
        fileContent: Response object or file content stored locally
                  
    Usage:
    
        This function connects to the Thingworx API endpoint
        to download files uploaded by the user to a custom
        project File Repository.
        
        The user will supply a repository name and file and
        the file will be downloaded locally. 
        IMPORTANT: This function works for text based files
        
         i.e. .py, .txt, .gcode files 
'''
def uploadFileToOctoprint(fileName:str, fileContent:str) -> bool:
    
    key = OPappKey
    
    # Create a unique boundary for the form body
    boundary = binascii.hexlify(os.urandom(16)).decode('ascii')
    
    # Form the body of the request
    body = (
         "".join("--%s\r\n"
                 "Content-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
                 "Content-Type: application/octet-stream\r\n"
                 "\r\n"
                 "%s\r\n" % (boundary, "file", fileName, fileContent)) +
             "--%s--\r\n" % boundary
        )

    # Define the content_type
    content_type = "multipart/form-data; boundary=%s" % boundary

    # Url parameters
    url = '/api/files/local'

    # Establish the headers and API key
    headers = {
        'X-Api-Key': key.strip('\n'),
        'Content-Type': content_type,
        'Content-Length': str(sys.getsizeof(body))
        }

    payload = body

    params = {}

    response = requests.request("POST", base+url, params=params, headers=headers, data=payload)
    print(response)