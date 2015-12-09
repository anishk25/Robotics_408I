import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import encoders
import motors

#right is master, left is slave
master_power = .6
slave_power = -.6
right_num_revs = 0
left_num_revs = 0
kp = .5

encoders.init()
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


old_x = 0
old_y = 0
old_z = 0
while True:
  if imu.IMURead():
    # x, y, z = imu.getFusionData()
    # print("%f %f %f" % (x,y,z))
    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    x = math.degrees(fusionPose[0])
    y = math.degrees(fusionPose[1])
    z = math.degrees(fusionPose[2])
    
    if(abs(x-old_x)>0.3 or abs(y-old_y)>0.3 or abs(z-old_z)>0.3):
        print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
    
    old_x = x
    old_y = y
    old_z = z	
    time.sleep(poll_interval*1.0/1000.0)
	
  try:
    print(str(right_num_revs)+"  "+str(left_num_revs))
    motors.speed(slave_power, master_power)
    adjustMotorPowers()
    readEncoder()
  except KeyboardInterrupt:
    break

motors.cleanup()
