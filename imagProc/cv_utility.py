import cv2
import numpy as np

def filterContours(contours,minArea,maxArea):
	filteredContours = []
	for contour in contours:
		area = cv2.contourArea(contour)
		if(area >= minArea and area <= maxArea):
			filteredContours.append(contour)
	return filteredContours


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


def getContoursForColor(img,lowerBound,upperBound,minContourArea,maxContourArea,dilImage = False):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	threshImg = cv2.inRange(imgHSV,lowerBound,upperBound)
	if(dilImage == True):
		kernel =np.ones((2,2),np.uint8)
		erodedDilImg = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, kernel)
		threshImg = erodedDilImg
	contours, hierarchy = cv2.findContours(threshImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	filterCont = filterContours(contours,minContourArea,maxContourArea)	
	return filterCont


def drawCirclesForContours(img,contours):
	for contr in contours:
		center,radius = getCircleFromContour(contr)
		center_in = (int(center[0]),int(center[1]))
		cv2.circle(img,center_in,int(radius),(0,255,0),2)

def drawCircleForPoints(img,pts,radius,color,lineLen):
	if(pts != None):
		for pt in pts:
			cv2.circle(img,pt,radius,color,lineLen)

def getCirclesFromContours(contours):
	circleList = []
	for contr in contours:
		center,radius = getCircleFromContour(contr)
		center_in = (int(center[0]),int(center[1]))
		radius_in = int(radius)
		circleList.append((center_in,radius_in))
	return circleList

def getCenterOfContours(contours):
	centerLst = []
	for contr in contours:
		moment = cv2.moments(contr)
		center = (moment['m10']/moment['m00'],moment['m01']/moment['m00'])
		center_in = (int(center[0]),int(center[1]))
		centerLst.append(center_in)
	return centerLst

def contourCompFun(c1,c2):
	return cv2.contourArea(c1) - cv2.contourArea(c2)

def sortContoursByArea(contours):
	contours.sort(cmp=contourCompFun)


