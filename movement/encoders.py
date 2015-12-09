import serial

ser = None

def init():
	global ser
	ser = serial.Serial('/dev/ttyACM0', 115200)

def read():
	global ser
	ser.write("r\n")
	in_str = ser.readline()
	buf = in_str.split('\t')
	return  float(buf[0])/4480.0, float(buf[1])/4480.0

def clear():
	global ser
	ser.write('c\n')
