from os import access
import time
import math
import serial
import sys
import glob
import json

##
##
## Define Serial Functions
##
##
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
        for port in ports:
            if 'usb' in port:
                guess = port                
                
        try:
            return guess
        except:
            print('no USB ports found')
            quit()
    elif sys.platform.startswith('linux'):
        ports = glob.glob('/dev/tty*')
        # usbPorts = []
        # for port in ports:
        #     if 'USB' in port:
        #         usbPorts.append(port)                
                
        # if len(usbPorts) == 0:
        #     print('no USB ports found')
        #     quit()
        # else:
        #     return usbPorts
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print('port found:'+result[0])
    return result[0]