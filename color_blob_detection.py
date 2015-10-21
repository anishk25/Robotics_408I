#http://docs.opencv.org/2.4.10/doc/tutorials/imgproc/shapedescriptors/bounding_rects_circles/bounding_rects_circles.html


import numpy as np
import cv2

def getThresholdedImageHSV(img):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	imgThresh = cv2.inRange(imgHSV,COLOR_MIN,COLOR_MAX)
	return imgThresh

def filterContours(contours):
	filteredContours = []
	for contour in contours:
		area = cv2.contourArea(contour)
		if(area >= MIN_CONTOUR_AREA):
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
	

def convertRGBColorToHSV(colorScalar):
	rgb_img = np.zeros((1,1,3),np.uint8)
	rgb_img[0,0] = colorScalar
	hsv_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
	print hsv_img[0,0]
	return hsv_img[0,0]

def convertHSVColorToRGB(colorScalar):
	hsv_img = np.zeros((1,1,3),np.uint8)
	hsv_img[0,0] = colorScalar
	rgb_img = cv2.cvtColor(hsv_img,cv2.COLOR_HSV2BGR)
	print rgb_img[0,0]
	return rgb_img[0,0]

def convertRGBColorToGray(colorScalar):
	rgb_img = np.zeros((1,1,3),np.uint8)
	rgb_img[0,0] = colorScalar
	gray_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2GRAY)
	print gray_img[0,0]
	return gray_img[0,0]



CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# color order is B,G,R !!!
#COLOR_MIN = convertRGBColorToHSV(np.array([5,50,50]))
#COLOR_MAX = convertRGBColorToHSV(np.array([15,255,255]))

COLOR_MIN = np.array([6,50,50]);
COLOR_MAX = np.array([14,255,255]);


MIN_CONTOUR_AREA = 20


videoCap = cv2.VideoCapture(0)
videoCap.set(CV_CAP_PROP_FRAME_WIDTH,640)
videoCap.set(CV_CAP_PROP_FRAME_HEIGHT,480)

if(videoCap.isOpened() != True):
	videoCap.open()


while(True):
	ret,frame = videoCap.read()
	imgThresh = getThresholdedImageHSV(frame)


	contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	lContour = getLargestContour(contours)

	if lContour != None:
		center,radius = getCircleFromContour(lContour)
		r_int = int(radius)
		center_in = (int(center[0]),int(center[1]))
		cv2.circle(frame,center_in,2,(0,255,0),3)
		#cv2.drawContours(frame, [lContour], -1, (0,255,0), 2);
	
	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break


videoCap.release()
cv2.destroyAllWindows()


