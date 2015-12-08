import cv2
import frameClick as fc
import numpy as np
import cv_utility as cvUtil


CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

TRANS_WIDTH = 640
TRANS_HEIGHT = 480



videoCap = cv2.VideoCapture(0)
videoCap.set(CV_CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
videoCap.set(CV_CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)

pointsArr = np.zeros((4,2),dtype=np.int)
quad_pts = np.zeros((4,2),dtype=np.int)

quad_pts[0] = (0,0)
quad_pts[1] = (TRANS_WIDTH,0)
quad_pts[2] = (TRANS_WIDTH,TRANS_HEIGHT)
quad_pts[3] = (0,TRANS_HEIGHT)


orderedPointsLst = []
orderedPointsArr = None
numCorners = 0

GREEN_LOW_HSV = np.array([55,250,250])
GREEN_HIGH_HSV = np.array([65,255,255])


def order_points(pts):
	ordPoints = []
	y_max_in = np.argmax(pts[:,1])
	y_min_in = np.argmin(pts[:,1])
	x_max_in = np.argmax(pts[:,0])
	x_min_in = np.argmin(pts[:,0])

	ordPoints.append(tuple(pts[x_min_in]))
	ordPoints.append(tuple(pts[y_max_in]))
	ordPoints.append(tuple(pts[x_max_in]))
	ordPoints.append(tuple(pts[y_min_in]))

	return ordPoints


def drawRectOnFrame(frame,pts):
	if(len(pts) == 4):
		cv2.line(frame,pts[0],pts[3],(0,255,0),1)
		for i in range(0,len(pts)-1):
			cv2.line(frame,pts[i],pts[i+1],(0,255,0),1)

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
			orderedPointsLst = order_points(pointsArr)
			orderedPointsArr = np.array(orderedPointsLst)
			print orderedPointsArr


def getTransFormImage(img,cornersInImg,wantedCorners,size):
	if(cornersInImg != None):
		transmtx = cv2.getPerspectiveTransform(cornersInImg.astype(np.float32),wantedCorners.astype(np.float32))
		return cv2.warpPerspective(img,transmtx,size)
	else:
		return None


cv2.namedWindow('frame')
cv2.setMouseCallback('frame',frameClickEvent)

#print(cvUtil.convertRGBColorToHSV((0,255,0)))

while(True):
	ret,frame = videoCap.read()
	drawRectOnFrame(frame,orderedPointsLst)
	transImage = getTransFormImage(frame,orderedPointsArr,quad_pts,(TRANS_WIDTH, TRANS_HEIGHT))

	cv2.imshow('frame',frame)
	if(transImage != None):
		cv2.imshow('tansImg',transImage)

	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break
