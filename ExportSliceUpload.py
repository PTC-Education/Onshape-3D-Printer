from OnshapePlus import *
from Octoprint import *

url = input('Input url of Part Studio you want to export as STL: ')
elementConfiguration = getElementConfiguration(url)
configString = ""
fileConfig = ""
for param in elementConfiguration['configurationParameters']:
    if param['typeName'] == "BTMConfigurationParameterEnum":
        options = "Options are: "
        for option in param['message']['options']:
            options = options + option['message']['option'] + ", "
        config = input("Input the configuration for the parameter named "+param['message']['parameterName']+" ("+options+"): ")
    else:
        config = input("Input the configuration for the parameter named "+param['message']['parameterName']+": ")
    configString = configString + param['message']['parameterId'] + "%3D" + config + ";"
    fileConfig = fileConfig + param['message']['parameterId'] + "_" + config

# print(configString)
partList = getPartsInPartStudio(url)
fileName = ""
for parts in partList:
    fileName = fileName + parts['name'] + "_"

## to fix: default filename
## 
# defaultFileName = fileName + fileConfig + '.stl'd
# filename = input("Click enter to export parts to filename '"+defaultFileName+"' or type a file name here: ")
# if filename == "":
#     exportSTL(url,defaultFileName,configString)
#     filename = defaultFileName
#     gcodefile = defaultFileName.replace(".stl",".gcode")
# else:
#     exportSTL(url,filename,configString)
#     gcodefile = filename.replace(".stl",".gcode")

filename = input("Enter a file name ending in .stl here: ")
exportSTL(url,filename,configString)
gcodefile = filename.replace(".stl",".gcode")

print('File successfully exported!')
print('Loaded 3D printer config files listed below...')
for file in os.listdir("./"):
    if file.endswith(".ini"):
        print(os.path.join("./", file))
printerConfig = input('Input the name of the config file you want to use for slicing: ')
if not "./" in printerConfig:
    printerConfig = "./" + printerConfig
# printerConfig = "colabConfigBundle.ini"

try:
    command = "slic3r-prusa3d --no-gui --load "+printerConfig+" "+filename
    # Suppress the output in order to not break the EMSSS
    suppress = " >/dev/null 2>&1"

    # Run the gcode generation and save output as a string
    os.system(command + suppress)
    s=""
    with open(gcodefile) as f: s = f.read()
    
    #upload Gcode string to Octopirnt and start print
    uploadFileToOctoprint(gcodefile, s)
    opStartPrint(gcodefile)
except:
    print('Failed at slicing. Please ensure prusa-slic3r is installed and your configuration file works.')
