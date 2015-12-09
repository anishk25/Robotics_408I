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

pointsArr = np.zeros((4,2),dtype=np.int)

quad_pts = np.zeros((4,2),dtype=np.int)
quad_pts[0] = (0,0)
quad_pts[1] = (TRANS_WIDTH,0)
quad_pts[2] = (TRANS_WIDTH,TRANS_HEIGHT)
quad_pts[3] = (0,TRANS_HEIGHT)

orderedPointsLst = []
orderedPointsArr = None
numCorners = 0

robots = []

first = True
heading = None
distance = None


def frameClickEvent(event,x,y,flags,param):
	global numCorners
	global pointsArr
	global orderedPointsLst
	global orderedPointsArr
	if event == cv2.EVENT_LBUTTONUP:
		if(numCorners < 4):
			print ((x,y))
			pointsArr[numCorners] = (x,y)
			numCorners += 1
		else:
			orderedPointsLst = scrTrans.order_points(pointsArr)
			orderedPointsArr = np.array(orderedPointsLst)
			print orderedPointsArr

#Takes a socket input
def client_handler(c, addr):
	global heading
	global distance
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
				waypoint = "w" + str(h) + "," + str(dist)
				print "Sending waypoint: " + waypoint
				c.sendall(waypoint.encode())
				send_waypoint = False




def vector_to_heading(vector):
	x, y = vector
	return np.angle([x + y*1.0j], deg=True)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 31415))

s.listen(5)

# cv2.namedWindow('frame')
# cv2.setMouseCallback('frame',frameClickEvent)

videoCap = cv2.VideoCapture(0)
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
	if first:
		cone = frameProcessor.getConeVector()
		robot = frameProcessor.getRobotVector()
		if cone != None and robot != None:
			cone_vec = vector_to_heading(cone)
			robot_vec = vector_to_heading(robot)
			x, y = cone
			distance = (x*x + y*y)**0.5
			heading = cone_vec - robot_vec
			first = False
			# print cone
			# print robot
			print cone_vec
			print robot_vec
			print cone_vec - robot_vec

	else:
		cone = frameProcessor.getConeVector()
		robot = frameProcessor.getRobotVector()
		if cone != None and robot != None:
			x, y = cone
			new_distance = (x*x + y*y)**0.5
			if(abs(new_distance - distance) > 200):
				cone_vec = vector_to_heading(cone)
				robot_vec = vector_to_heading(robot)
				# print cone
				# print robot
				print cone_vec
				print robot_vec
				print cone_vec - robot_vec
				distance = new_distance
				heading = cone_vec - robot_vec

	#print frameProcessor.getRobotVector()
	#print frameProcessor.getConeVector()

	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break
