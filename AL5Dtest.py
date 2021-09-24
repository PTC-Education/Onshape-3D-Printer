from SerialSetup import *

port = serial_ports()

portname = input('Ports found listed above. Enter name of port for robot arm: ')
ser = serial.Serial(
    port=portname,
    baudrate=9600
)

ser.isOpen()

time.sleep(2)

ser.close()