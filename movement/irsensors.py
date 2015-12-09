import RPi.GPIO as GPIO

IR_LEFT = 22
IR_RIGHT = 27

def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(IR_LEFT, GPIO.IN)
	GPIO.setup(IR_RIGHT, GPIO.IN)

def read():
	return GPIO.input(IR_LEFT), GPIO.input(IR_RIGHT)
