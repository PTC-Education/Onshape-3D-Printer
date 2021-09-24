from OnshapePlus import *

url = input('Input url of Part Studio you want to export as STL: ')
print('default configuration for token = "CoinText%3DMatt%3BList_Os3Ch7CJl5rv3f%3DPTC"')
configurationText = input('Input the configuration text (just click enter if there are none): ')
filename = input('Input the filename for the stl (just click enter if you want to use "OnshapePart.stl"): ')
# try:
print(exportSTL(url,filename,'CoinText%3D'+configurationText))
# except:
#     print('fail')
