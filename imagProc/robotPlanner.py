import cv2
import numpy as np
import screen_transformer as scrTrans
from frameProcessor import FrameProcessor
import socket
import threading


FRAME_WIDTH = 640
FRAME_HEIGHT = 480

TRANS_WIDTH = 640
TRANS_HEIGHT = 480


robots = []

first = True
heading = None
distance = None

point = None
hasPoint = False


def frameClickEvent(event,x,y,flags,param):
	global hasPoint
	global point
	if event == cv2.EVENT_LBUTTONUP:
		point = (x,y)
		hasPoint = True
		print "Clicked at point",
		print point


#Takes a socket input
def client_handler(c, addr):
	global heading
	global distance
	global hasPoint
	address, port = addr
	send_waypoint = True
	print('Incoming Connection')
	c.setblocking(0)
	while 1:
		try:
			reply = c.recv(4096).decode()
		except socket.error, e:
			pass

		else:
			if not reply == '':
				if reply[0] == 'r':
					if not address in robots:
						robots.append(address)
						print('Registered Robot at ' + address)
				elif reply[0] == 'o':
					print('Robot at ' + address + ' encountered obstacle')
				elif reply[0] == 's':
					send_waypoint = True

		if send_waypoint:
			if heading != None and distance != None:
				h = heading
				dist = (distance*12.0)/(1920.0)
				if dist > 1:
					dist = 1.0
				if dist > 0.41:
					waypoint = "w" + str(h) + "," + str(dist)
					print "Sending waypoint: " + waypoint
					c.sendall(waypoint.encode())
					send_waypoint = False
					hasPoint = False




def vector_to_heading(vector):
	x, y = vector
	return np.angle([x + y*1.0j], deg=True)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 31415))

s.listen(5)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame',frameClickEvent)

videoCap = cv2.VideoCapture(1)
videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)

frameProcessor = FrameProcessor()

def handle_connections():
	(clientsocket, address) = s.accept()
	cli = threading.Thread(target=client_handler(clientsocket, address))
	cli.setDaemon(True)
	cli.start()

con = threading.Thread(target=handle_connections)
con.setDaemon(True)
con.start()

while(True):

	ret,frame = videoCap.read()

	#frameProcessor.processFrame(transImage)
	frameProcessor.processFrame(frame)

	if hasPoint:
		pos = frameProcessor.getRobotPosition()
		if point != None and pos != None:
			vec = (point[0] - pos[0], (point[1] - pos[1])*-1)
			#print vec
			angle = vector_to_heading(vec)
			robot = frameProcessor.getRobotVector()
			robot_vec = vector_to_heading(robot)
			x, y = vec
			distance = (x*x + y*y)**0.5
			heading = robot_vec - angle
			# print distance
			#print heading
	else:
		if first:
			cone = frameProcessor.getConeVector()
			robot = frameProcessor.getRobotVector()
			# print cone
			# print robot
			if cone and robot:
				cone_vec = vector_to_heading(cone)
				robot_vec = vector_to_heading(robot)
				x, y = cone
				distance = (x*x + y*y)**0.5
				heading = cone_vec - robot_vec
				first = False
				# print cone
				# print robot
				# print cone_vec
				# print robot_vec
				print cone_vec - robot_vec

		else:
			cone = frameProcessor.getConeVector()
			robot = frameProcessor.getRobotVector()
			# print ssobot
			# print cone
			# print robot
			if cone and robot:
				x, y = cone
				new_distance = (x*x + y*y)**0.5
				dist_in_feet = (new_distance*12.0)/1920.0
				#print dist_in_feet
				if(abs(new_distance - distance) < 200):
					cone_vec = vector_to_heading(cone)
					robot_vec = vector_to_heading(robot)
					# print cone
					# print robot
					#print cone_vec
					#print robot_vec
					distance = new_distance
					heading = robot_vec - cone_vec
					#print heading

		#print frameProcessor.getRobotVector()
		#print frameProcessor.getConeVector()

	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		s.shutdown(socket.SHUT_RDWR)
		exit()
		break
	elif(cv2.waitKey(1) & 0xFF == ord('n')):
		first = True
