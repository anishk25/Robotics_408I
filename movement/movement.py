import sys, getopt

sys.path.append('.')
import os.path
import time
import math
import encoders
import motors

#number of wheel rotations the master must lag the slave before the robot decides to kill whatever's in the way
kill_threshold = 1



#input angle in degrees, input distance in feet
angle = 90.0
distance = 40.0

distance = 40.0

#constants in feet
diameter = 11.25
wheel_circumference = 16.72

#right is master, left is slave
master_power = .25
slave_power = -.25
right_num_revs = 0
left_num_revs = 0
kp = .5

#distance modifier
d_mod = .95

turns= angle/360.0*math.pi*diameter/wheel_circumference
dist = distance/wheel_circumference

#encoders.init()
#encoders.clear()
#motors.init()

en_left, en_right = 0.0,0.0




def adjustMotorPowers():
	global slave_power
	global en_left
	global en_right
	global kp

	error = en_right + en_left
	slave_power -= error/kp
	encoders.clear()
	time.sleep(.1)

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

def adjustMotorPowers_straight():
	global slave_power
	global en_left
	global en_right
	global kp
	
	error = en_right - en_left
	slave_power -= error/(kp*4)
	encoders.clear()
	time.sleep(.01)

def readEncoder_straight():
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



def go(given_angle, given_distance):
	angle = given_angle
	distance = given_distance
	curr_time = time.time()
	next_state = False
	
	#constants in feet
	diameter = 11.25
	wheel_circumference = 16.72

	#right is master, left is slave
	global slave_power
	global master_power
	master_power = .25
	slave_power = -.25
	global right_num_revs
	right_num_revs= 0
	global left_num_revs
	left_num_revs = 0
	global kp
	kp = .5

	#distance modifier
	d_mod = .95

	turns= angle/360.0*math.pi*diameter/wheel_circumference
	dist = distance/wheel_circumference
	
	encoders.init()
	encoders.clear()
	motors.init()
	
	global en_right
	global en_left
	en_left, en_right = encoders.read()


	while True:
		try:
			if(abs(right_num_revs)+abs(left_num_revs))/2.0 >= turns*d_mod and not next_state:
				print slave_power
				print master_power
				curr_time=time.time()
				next_state = True
			
				if time.time()>(curr_time + 0) and next_state:
					break
		
			motors.speed(slave_power, master_power)
			adjustMotorPowers()
			readEncoder()
		except KeyboardInterrupt:
			break

	motors.speed(0,0)
	time.sleep(1)

	kill_constant = 5
	right_num_revs = 0.0
	left_num_revs = 0.0
	slave_power = 0.233
	master_power = 0.25

	while True:
		if (abs(right_num_revs)+abs(left_num_revs))/2.0 >= dist*d_mod:
			break
		try:    
			if(abs(left_num_revs)-abs(right_num_revs)) > kill_threshold:
				master_power += .95*master_power + .05*kill_constant
			print(str(right_num_revs)+"  "+str(left_num_revs))
			motors.speed(slave_power, master_power)
			adjustMotorPowers_straight()
			readEncoder_straight()
			print "Slave Speed: "+str(slave_power), "Master Speed: "+str(master_power)
		except KeyboardInterrupt:
			break

	motors.cleanup()
