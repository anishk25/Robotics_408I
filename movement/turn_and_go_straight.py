import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import encoders
import motors

#input angle in degrees, input distance in feet
angle = 90.0
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

encoders.init()
encoders.clear()
motors.init()

en_left, en_right = encoders.read()

SETTINGS_FILE = "RTIMULib"

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
	slave_power += error/(kp*200)
	#encoders.clear()
	time.sleep(.001)

def readEncoder_straight():
	global en_left
	global en_right
	global right_num_revs
	global left_num_revs

	new_en_left, new_en_right = encoders.read()
	if(new_en_right != en_right or new_en_left != en_left):
		en_right = new_en_right
		right_num_revs = en_right
		en_left = new_en_left
		left_num_revs = en_left		

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)
curr_time = time.time()
next_state = False
while True:
  try:
    if(abs(right_num_revs)+abs(left_num_revs))/2.0 >= turns*d_mod and not next_state:
        #print(str(right_num_revs)+"  "+str(left_num_revs))
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
encoders.clear()

right_num_revs = 0.0
left_num_revs = 0.0
slave_power = 0.25
master_power = 0.25
target_power = 0.6
alpha = .95
while True:
    if (abs(right_num_revs)+abs(left_num_revs))/2.0 >= dist*d_mod:
        break
    try:    
        print(str(right_num_revs)+"  "+str(left_num_revs))
        while(master_power < target_power and (abs(right_num_revs)+abs(left_num_revs))/2.0 < dist*d_mod):
            master_power = alpha*master_power + (1-alpha)*target_power
            print(str(right_num_revs)+"  "+str(left_num_revs))
			#slave_power = alpha*master_power + (1-alpha)*target_power
            #motors.speed(slave_power, master_power)
            adjustMotorPowers_straight()
            motors.speed(slave_power, master_power)
            readEncoder_straight()
		
        print "got out of loop"
        adjustMotorPowers_straight()
        motors.speed(slave_power, master_power)
        #adjustMotorPowers_straight()
        readEncoder_straight()
    except KeyboardInterrupt:
        break

motors.cleanup()
