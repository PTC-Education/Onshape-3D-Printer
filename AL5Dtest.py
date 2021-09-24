from SerialSetup import *

port = serial_ports()
ser = serial.Serial(
    port=port,
    baudrate=9600
)

ser.isOpen()

time.sleep(2)

ser.close()