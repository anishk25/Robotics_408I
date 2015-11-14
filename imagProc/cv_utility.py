import cv2

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


def getContoursForColor(img,lowerBound,upperBound,minContourArea,maxContourArea):
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	threshImg = cv2.inRange(imgHSV,lowerBound,upperBound)
	contours, hierarchy = cv2.findContours(threshImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	filterCont = filterContours(contours,minContourArea,maxContourArea)	
	return filterCont


def drawCirclesForContours(img,contours):
	for contr in contours:
		center,radius = getCircleFromContour(contr)
		center_in = (int(center[0]),int(center[1]))
		cv2.circle(img,center_in,int(radius),(0,0,255),1)

def getCenterOfContours(contours):
	centerLst = []
	for contr in contours:
		moment = cv2.moments(contr)
		center = (moment['m10']/moment['m00'],moment['m01']/moment['m00'])
		center_in = (int(center[0]),int(center[1]))
		centerLst.append(center_in)
	return centerLst


