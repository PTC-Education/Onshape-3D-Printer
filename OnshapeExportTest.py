from OnshapePlus import *

url = input('Input url of Part Studio you want to export as STL: ')
try:
    print(exportSTL(url))
except:
    print('fail')

