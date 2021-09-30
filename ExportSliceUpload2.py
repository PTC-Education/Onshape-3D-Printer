from OnshapePlus import *
from Octoprint import *


url = input('Input url of Part Studio you want to export as STL: ')
# print('default configuration for token = "CoinText%3DMatt%3BList_Os3Ch7CJl5rv3f%3DPTC"')
# configurationText = input('Input the configuration text (just click enter if there are none): ')
# logoChoice = input('Do you want PTC or Onshape logo on the back?: ')
filename = input('Input the filename for the stl (just click enter if you want to use "OnshapePart.stl"): ')
printerConfig = input('Input the name of your 3D printer config file: ')
# printerConfig = "colabConfigBundle.ini"

# try:
# if logoChoice == "PTC":
#     exportSTL(url,filename,'CoinText%3D'+configurationText+'%3BList_Os3Ch7CJl5rv3f%3D'+logoChoice)
# else:
#     exportSTL(url,filename,'CoinText%3D'+configurationText)
exportSTL(url,filename)
command = "slic3r-prusa3d --no-gui --load "+printerConfig+" "+filename
# Suppress the output in order to not break the EMSSS
suppress = " >/dev/null 2>&1"

# Run the gcode generation and 
os.system(command + suppress)
s=""
gcodefile = filename.replace(".stl",".gcode")
with open(gcodefile) as f: s = f.read()

uploadFileToOctoprint(gcodefile, s)
opStartPrint(gcodefile)
# except:
#     print('fail')
