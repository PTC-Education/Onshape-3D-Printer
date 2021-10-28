from OnshapePlus import *

url = input('Input url of Part Studio you want to export as STL: ')
elementConfiguration = getElementConfiguration(url)
configString = ""
fileConfig = ""
for param in elementConfiguration['configurationParameters']:
    config = input("Input the configuration for the parameter named "+param['message']['parameterName']+": ")
    configString = configString + param['message']['parameterId'] + "%3D" + config
    fileConfig = fileConfig + param['message']['parameterId'] + "_" + config

print(configString)
partList = getPartsInPartStudio(url)
fileName = ""
for parts in partList:
    fileName = fileName + parts['name'] + "_"

defaultFileName = fileName + fileConfig + ".stl"
filename = input('Click enter to export parts to filename "'+defaultFileName+'" or type a file name here: ')
if filename == "":
    exportSTL(url,defaultFileName,configString)
else:
    exportSTL(url,filename,configString)
# except:
#     print('fail')
