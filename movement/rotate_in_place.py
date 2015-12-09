import encoders
import motors
from time import sleep
#right is master, left is slave
master_power = .35
slave_power = .45
right_num_revs = 0
left_num_revs = 0
kp = .5

encoders.init()
motors.init()

en_left, en_right = encoders.read()

def adjustMotorPowers():
	global slave_power
	global en_left
	global en_right
	global kp

	error = en_right + en_left
	slave_power -= error/kp
	encoders.clear()
	sleep(.1)

def readEncoder():
	global en_left
	global en_right
	global right_num_revs
	global left_num_revs

	new_en_left, new_en_right = encoders.read()
	if(new_en_right != en_right or new_en_left != en_left):
		en_right = new_en_right
		right_num_revs += en_right
		en_left = new_en_left
		left_num_revs += en_left

while(True):
	try:
		print(str(right_num_revs)+"  "+str(left_num_revs))
		motors.speed(slave_power, master_power)
		#adjustMotorPowers()
		#readEncoder()
	except KeyboardInterrupt:
		break

motors.cleanup()
