import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"
imu = None

def init():
	global SETTING_FILE
	global imu
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
	#print("Recommended Poll Interval: %dmS\n" % poll_interval)

def read():
	global imu
	while True:
		if imu.IMURead():
			data = imu.getIMUData()
			print data
			fusionPose = data["fusionPose"]
			return fusionPose

init()
read()
