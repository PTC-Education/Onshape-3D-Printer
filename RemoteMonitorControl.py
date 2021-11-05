from OnshapePlus import *
from Octoprint import *

url = input("Enter the URL of the Document: ")
elements = OnshapeElement(url)

elementList = documentElementsList(url)
appElementId = ""
for element in elementList:
    if element['elementType'] == "APPLICATION" and element['name'] == "Octoprint AppElement":
        print("Found Octoprint App Element!")
        appElementId = element['id']
    else:
        pass

if appElementId == "":
    print("Created Octoprint App Element!")
    appElement = addAppElement(url)
    appElementId = appElement['elementId']

appElementUrl = url.replace(elements.eid,appElementId)
time.sleep(1)
jsonTree = getJsonTree(appElementUrl)

jobInfo = opJobInfo()
printerInfo = opInfo()
# print(printerInfo['state']['text'])
image = getOctoprintImage()

time.sleep(1)
updateAppElementJsonKey(appElementUrl,"image",image)
updateAppElementJsonKey(appElementUrl,"printerInfo",printerInfo)
updateAppElementJsonKey(appElementUrl,"jobInfo",jobInfo)

while True:
    jsonTree = getJsonTree(appElementUrl)
    print(jsonTree['tree']['updateInfo'])
    print(jsonTree['tree']['printQueue'])
    if jsonTree['tree']['updateInfo'] == "update":
        updateAppElementJsonKey(appElementUrl,"image",getOctoprintImage())
        updateAppElementJsonKey(appElementUrl,"printerInfo",opInfo())
        updateAppElementJsonKey(appElementUrl,"jobInfo",opJobInfo())
        updateAppElementJsonKey(appElementUrl,"updateInfo","waiting")
    
    if jsonTree['tree']['printerCommand'] == "home":
        opHome()
    elif jsonTree['tree']['printerCommand'] == "preheatPLA":
        opPreheatBedPLA()
        opPreheatToolPLA()
    elif jsonTree['tree']['printerCommand'] == "unheat":
        opUnheatToolBed()
    elif jsonTree['tree']['printerCommand'] == "startNextInQueue":
        partStudioUrl = url.replace(elements.eid,jsonTree['tree']['printQueue'][0]['eid'])
        exportSliceUpload(partStudioUrl,jsonTree['tree']['printQueue'][0]['config'],"Ender3config.ini")

        
    time.sleep(10)

