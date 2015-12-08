import cv2
import numpy as np
import screen_transformer as scrTrans
from frameProcessor import FrameProcessor

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

cv2.namedWindow('frame')
cv2.setMouseCallback('frame',frameClickEvent)

videoCap = cv2.VideoCapture(0)
videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)

frameProcessor = FrameProcessor()

while(True):
	ret,frame = videoCap.read()
	scrTrans.drawRectOnFrame(frame,orderedPointsLst)
	transImage = scrTrans.getTransFormImage(frame,orderedPointsArr,quad_pts,(TRANS_WIDTH, TRANS_HEIGHT))

	cv2.imshow('frame',frame)
	if(transImage != None):
		print frameProcessor.getRobotAngle()
		cv2.imshow('transImage',transImage)

	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break






