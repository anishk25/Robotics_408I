from __future__ import division
import motors
from time import sleep

motors.init()

for i in xrange(0, 1000):
	motors.speed(i/1000, 0)
	sleep(0.001)	

for i in xrange(0, 1000):
	motors.speed(1, i/1000)
	sleep(0.001)

for i in xrange(0, 1000):
	motors.speed(1, 1 - i/1000)
	sleep(0.001)

for i in xrange(0, 1000):
	motors.speed(1 - i/1000, 0)
	sleep(0.001)

motors.cleanup()
