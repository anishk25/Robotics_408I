#http://docs.opencv.org/2.4.10/doc/tutorials/imgproc/shapedescriptors/bounding_rects_circles/bounding_rects_circles.html


import numpy as np
import cv2
import math

COLOR_MIN = np.array([6,50,50]);
COLOR_MAX = np.array([14,255,255]);

MIN_CONTOUR_AREA = 100

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

captureNum = 0

CAMERA_ANGLE_OF_VIEW_HORIZ = 53.5
RADIANS_PER_PIX_X = math.radians(CAMERA_ANGLE_OF_VIEW_HORIZ)/FRAME_WIDTH
DEGRESS_PER_PIX_X = CAMERA_ANGLE_OF_VIEW_HORIZ/FRAME_WIDTH
CENTER_OF_FRAME = (FRAME_WIDTH/2,FRAME_HEIGHT/2)
FONT = cv2.FONT_HERSHEY_SIMPLEX
kernel =np.ones((2,2),np.uint8)
frame = None


def filterContours(contours,minArea):
	filteredContours = []
	for contour in contours:
		area = cv2.contourArea(contour)
		if(area >= minArea):
			filteredContours.append(contour)
	return filteredContours

def getLargestContour(contours):
	if(len(contours) > 0):
		largestContour = contours[0]
		largestArea = cv2.contourArea(largestContour)
		for contour in contours:
			area = cv2.contourArea(contour)
			if(area > largestArea):
				largestArea = area
				largestContour = contour
		return largestContour
	return None

def getCircleFromContour(contour):
	approxCurve = cv2.approxPolyDP(contour,3,True);
	center,radius = cv2.minEnclosingCircle(approxCurve)
	return center,radius

def drawAngleOfContours(contours,frame):
	for contour in contours:
		#center,radius = getCircleFromContour(contour)
		moment = cv2.moments(contour)
		center = (moment['m10']/moment['m00'],moment['m01']/moment['m00'])
		dist_x = center[0]-CENTER_OF_FRAME[0]
		angle = dist_x * DEGRESS_PER_PIX_X
		center_in = (int(center[0]),int(center[1]))
		cv2.putText(frame,str(int(angle)),center_in,FONT, 1,(0,255,0),2)
		#r_int = int(radius)
		cv2.circle(frame,center_in,2,(255,0,0),3)


def getContoursForColor(blurredImg,lowerBound,upperBound,erodeKernel):
	threshImg = cv2.inRange(blurredImg,lowerBound,upperBound)
	erodedDilImg = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, erodeKernel)
	contours, hierarchy = cv2.findContours(erodedDilImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	filterCont = filterContours(contours,MIN_CONTOUR_AREA)	
	return filterCont

def convertRGBColorToHSV(colorScalar):
	rgb_img = np.zeros((1,1,3),np.uint8)
	rgb_img[0,0] = colorScalar
	hsv_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
	print hsv_img[0,0]
	return hsv_img[0,0]

# for capturing frames
def frameClickEvent(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONUP:
		cv2.imwrite('./contourAngle' + str(x)+ '.jpg', frame)



videoCap = cv2.VideoCapture(0)
videoCap.set(CV_CAP_PROP_FRAME_WIDTH,640)
videoCap.set(CV_CAP_PROP_FRAME_HEIGHT,480)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame',frameClickEvent)

if(videoCap.isOpened() != True):
	videoCap.open()


while(True):
	ret,frame = videoCap.read()

	imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	blurredImg = cv2.GaussianBlur(imgHSV,(19,19),0,0)

	# get orange contours
	o_contours = getContoursForColor(blurredImg,np.array([0,100,200]),np.array([20,160,255]),kernel)

	# get black contours
	#b_contours = getContoursForColor(blurredImg,np.array([0,0,0]),np.array([255,160,20]),kernel)


	cv2.drawContours(frame,o_contours,-1,(0,255,0),2)
	#drawAngleOfContours(o_contours,frame)

	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break


videoCap.release()
cv2.destroyAllWindows()


