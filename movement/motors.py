import wiringpi2 as wiringpi
import RPi.GPIO as GPIO


''' DO NOT MODIFY VALUES '''

LEFT_MOTOR_PWM = 18
LEFT_MOTOR_A = 4
LEFT_MOTOR_B = 17 

RIGHT_MOTOR_PWM = 13
RIGHT_MOTOR_A = 16
RIGHT_MOTOR_B = 19

MAX_SPEED = 512
CLK_DIVISOR = 2

''' Public Functions '''

def init():
	GPIO.setmode(GPIO.BCM)
	wiringpi.wiringPiSetupGpio()
	wiringpi.pinMode(LEFT_MOTOR_PWM, 2)
	wiringpi.pinMode(RIGHT_MOTOR_PWM, 2)
	wiringpi.pwmSetMode(0)
	wiringpi.pwmSetClock(CLK_DIVISOR)
	wiringpi.pwmSetRange(MAX_SPEED)
	wiringpi.pwmWrite(LEFT_MOTOR_PWM, 0)
	wiringpi.pwmWrite(RIGHT_MOTOR_PWM, 0)
	GPIO.setup(LEFT_MOTOR_A, GPIO.OUT)
	GPIO.setup(LEFT_MOTOR_B, GPIO.OUT)	
	GPIO.setup(RIGHT_MOTOR_A, GPIO.OUT)
	GPIO.setup(RIGHT_MOTOR_B, GPIO.OUT)

def cleanup():
	wiringpi.pwmWrite(LEFT_MOTOR_PWM, 0)
	wiringpi.pwmWrite(RIGHT_MOTOR_PWM, 0)
	wiringpi.pinMode(LEFT_MOTOR_PWM, 0)
	wiringpi.pinMode(RIGHT_MOTOR_PWM, 0)
	GPIO.output(LEFT_MOTOR_A, GPIO.LOW)
	GPIO.output(LEFT_MOTOR_B, GPIO.LOW)	
	GPIO.output(RIGHT_MOTOR_A, GPIO.LOW)
	GPIO.output(RIGHT_MOTOR_B, GPIO.LOW)
	GPIO.setup(LEFT_MOTOR_A, GPIO.IN)
	GPIO.setup(LEFT_MOTOR_B, GPIO.IN)	
	GPIO.setup(RIGHT_MOTOR_A, GPIO.IN)
	GPIO.setup(RIGHT_MOTOR_B, GPIO.IN)

def speed(left, right):
	left_a = GPIO.LOW
	left_b = GPIO.LOW
	left_pwm = abs(left)

	right_a = GPIO.LOW
	right_b = GPIO.LOW
	right_pwm =abs(right)

	if left < 0:
		left_a = GPIO.HIGH
	elif left > 0:
		left_b = GPIO.HIGH
	
	if right < 0:
		right_a = GPIO.HIGH
	elif right > 0:
		right_b = GPIO.HIGH

	if(left_pwm > 1):
		left_pwm = MAX_SPEED
	else:
		left_pwm = int(left_pwm*MAX_SPEED)
	if right_pwm > 1:
		right_pwm = MAX_SPEED
	else:
		right_pwm = int(right_pwm*MAX_SPEED)
	
	GPIO.output(LEFT_MOTOR_A, left_a)
	GPIO.output(LEFT_MOTOR_B, left_b)
	GPIO.output(RIGHT_MOTOR_A, right_a)
	GPIO.output(RIGHT_MOTOR_B, right_b)
	wiringpi.pwmWrite(LEFT_MOTOR_PWM, left_pwm)
	wiringpi.pwmWrite(RIGHT_MOTOR_PWM, right_pwm)
