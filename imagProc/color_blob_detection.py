#http://docs.opencv.org/2.4.10/doc/tutorials/imgproc/shapedescriptors/bounding_rects_circles/bounding_rects_circles.html


import numpy as np
import cv2
import math

COLOR_MIN = np.array([6,50,50]);
COLOR_MAX = np.array([14,255,255]);

MIN_CONTOUR_AREA = 1500

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 

FRAME_WIDTH = 640
FRAME_HEIGHT = 480



CAMERA_ANGLE_OF_VIEW_HORIZ = 53.5
RADIANS_PER_PIX_X = math.radians(CAMERA_ANGLE_OF_VIEW_HORIZ)/FRAME_WIDTH
DEGRESS_PER_PIX_X = CAMERA_ANGLE_OF_VIEW_HORIZ/FRAME_WIDTH
CENTER_OF_FRAME = (FRAME_WIDTH/2,FRAME_HEIGHT/2)
FONT = cv2.FONT_HERSHEY_SIMPLEX


def getHSVChannel(img,index):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	return imgHSV[:,:,index]


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
		cv2.putText(frame,str(angle),center_in,FONT, 1,(0,255,0),2)
		#r_int = int(radius)
		cv2.circle(frame,center_in,2,(255,0,0),3)


def convertRGBColorToHSV(colorScalar):
	rgb_img = np.zeros((1,1,3),np.uint8)
	rgb_img[0,0] = colorScalar
	hsv_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
	print hsv_img[0,0]
	return hsv_img[0,0]

def checkForTriangles(contours):
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
		print len(approx)


videoCap = cv2.VideoCapture(0)
videoCap.set(CV_CAP_PROP_FRAME_WIDTH,640)
videoCap.set(CV_CAP_PROP_FRAME_HEIGHT,480)

if(videoCap.isOpened() != True):
	videoCap.open()


#kernel = np.array([[0,1,0],[1,1,1],[0,1,0]],np.uint8);
kernel = np.ones((6,6),np.uint8)

while(True):
	ret,frame = videoCap.read()
	hChannelImg = getHSVChannel(frame,0)
	sChannelImg = getHSVChannel(frame,1)

	blurredHImg = cv2.GaussianBlur(hChannelImg,(11,11),0,0)
	blurredSImg = cv2.GaussianBlur(sChannelImg,(11,11),0,0)


	hThreshImg = cv2.inRange(blurredHImg,4,7)
	sThreshImg = cv2.inRange(blurredSImg,155,255)
	combImg = cv2.bitwise_and(hThreshImg,sThreshImg)
	erodedDilImg = cv2.morphologyEx(combImg, cv2.MORPH_OPEN, kernel)
	corners = cv2.cornerHarris(erodedDilImg,2,3,0.04);

	contours, hierarchy = cv2.findContours(erodedDilImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	filterCont = filterContours(contours,MIN_CONTOUR_AREA)	
	checkForTriangles(filterCont)

	#cv2.drawContours(frame,filterCont,-1,(0,255,0),2)
	drawAngleOfContours(filterCont,frame)

	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break


videoCap.release()
cv2.destroyAllWindows()


