import cv2
import numpy as np
import frameClick as fc
import cv_utility as cvUtil
import math
import operator

largestArea = 0

BLUE_LOW_HSV = np.array([60,0,200])
BLUE_HIGH_HSV = np.array([120,60,255])

YELLOW_LOW_HSV = np.array([20,0,220])
YELLOW_HIGH_HSV = np.array([35,20,255])

PURPLE_LOW_HSV = np.array([130,0,240])
PURPLE_HIGH_HSV = np.array([160,25,255])

RED_LOW_HSV = np.array([0,0,240])
RED_HIGH_HSV = np.array([20,10,255])

MIN_CONTOUR_AREA = 10
MAX_CONTOUR_AREA = 250

def getDist(pt1,pt2):
	n1 = (pt2[1] - pt1[1])**2
	n2 = (pt2[0] - pt1[0])**2
	return math.sqrt(n1 + n2)
	

def distBetweenLineAndPt(pt,linePt1,linePt2):
	n1 = (linePt2[1]-linePt1[1])*pt[0]
	n2 = (linePt2[0]-linePt2[0])*pt[1]
	n3 = linePt2[0]*linePt1[1]
	n4 = linePt2[1]*linePt1[0]
	lineLen = getDist(linePt1,linePt2)
	if(lineLen <= 0):
		return -10
	dist = abs(n1 - n2 + n3 - n4)/lineLen
	return dist

def getAreaOfTriangle(triPts):
	assert(len(triPts) == 3)
	n1 = triPts[0][0]*(triPts[1][1] - triPts[2][1])
	n2 = triPts[1][0]*(triPts[2][1] - triPts[0][1])
	n3 = triPts[2][0]*(triPts[0][1] - triPts[1][1])
	area = abs(n1+n2+n3)/2
	return area

def getClosestPt(triPts, allPts):
	assert(len(triPts) == 3 and len(allPts) > 3)
	allPtsLen = len(allPts)
	pt1 = triPts[0]
	pt2 = triPts[1]
	minDist = 100000000
	minPt = (-1,-1)
	for i in range(0,allPtsLen):
		if(allPts[i] != pt1 and allPts[i] != pt2):
			dist = distBetweenLineAndPt(allPts[i],pt1,pt2)
			if(dist < minDist):
				minDist = dist
				minPt = allPts[i]
	return minPt

def largestTriangleHelper(allPointsList,trianglePtList,lrgTriPtList,currIndex,numPtsCovered):
	if(numPtsCovered < 3):
		for i in range(currIndex,len(allPointsList)):
			trianglePtList.append(allPointsList[i])
			largestTriangleHelper(allPointsList,trianglePtList,lrgTriPtList,i+1,numPtsCovered+1)
			trianglePtList.pop()
	else:
		global largestArea
		area = getAreaOfTriangle(trianglePtList)
		if(area > largestArea):
			del lrgTriPtList[:]
			largestArea = area
			lrgTriPtList.extend(trianglePtList)

def getLargestTriangle(allPointsList):
	trianglePtList = []
	lrgTriPtList = []
	largestTriangleHelper(allPointsList,trianglePtList,lrgTriPtList,0,0)
	return lrgTriPtList

def getSortedPtListInTri(basePt,triPts):
	assert(len(triPts) == 3)
	distDict = {}
	for i in range(0,len(triPts)):
		distDict[triPts[i]] = getDist(basePt,triPts[i])

	sortedPts = sorted(distDict.items(),key=operator.itemgetter(1))
	ptList = []
	for item in sortedPts:
		ptList.append(item[0])
	return ptList

def drawDirectionalTriangle(img,sortedTriPts):
	 assert(len(sortedTriPts) == 3)
	 # draw green line at base
	 cv2.line(img,sortedPts[0],sortedPts[1],(0,255,0),2)
	 # draw red line for other two sides
	 cv2.line(img,sortedPts[0],sortedPts[2],(0,0,255),2)
	 cv2.line(img,sortedPts[1],sortedPts[2],(0,0,255),2)




imageFileName = 'blue_top_down.jpg'
topDownPrefix = './TestImages/TopDown/'
sidePrefix = './TestImages/Side/'
topDownImages = np.array(['blue.jpg','yellow.jpg','red.jpg','purple.jpg','purple2.jpg'])
sideImages = np.array(['blue.jpg','red.jpg','purple.jpg','purple2.jpg'])


ledImage = cv2.imread(topDownPrefix+topDownImages[2],cv2.CV_LOAD_IMAGE_COLOR)
imgShape = ledImage.shape
aspectRatio = float(imgShape[1])/float(imgShape[0])
newHeight = 700
newWidth = int(newHeight*aspectRatio)
ledImage = cv2.resize(ledImage,(newWidth,newHeight))

selectLowHSV = RED_LOW_HSV
selectHighHSV = RED_HIGH_HSV

#imgHSV = cv2.cvtColor(ledImage,cv2.COLOR_BGR2HSV)
#threshImg = cv2.inRange(imgHSV,selectLowHSV,selectHighHSV)

contours = cvUtil.getContoursForColor(ledImage,selectLowHSV,selectHighHSV,MIN_CONTOUR_AREA,MAX_CONTOUR_AREA)
centerLst = cvUtil.getCenterOfContours(contours)

largestArea = 0
lrgTriPtList = getLargestTriangle(centerLst)
baseCenterPt = getClosestPt(lrgTriPtList,centerLst)
sortedPts = getSortedPtListInTri(baseCenterPt,lrgTriPtList)
drawDirectionalTriangle(ledImage,sortedPts)


cv2.namedWindow('ledImage')
cv2.setMouseCallback('ledImage',fc.frameClickEvent,ledImage)

while(True):
	cv2.imshow('ledImage',ledImage)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break