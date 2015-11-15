import cv2
import numpy as np
import frameClick as fc
import cv_utility as cvUtil
import algorithms
import sys

BLUE_LOW_HSV = np.array([60,0,200])
BLUE_HIGH_HSV = np.array([120,60,255])

YELLOW_LOW_HSV = np.array([20,0,220])
YELLOW_HIGH_HSV = np.array([35,20,255])

PURPLE_LOW_HSV = np.array([130,0,240])
PURPLE_HIGH_HSV = np.array([160,25,255])

RED_LOW_HSV = np.array([0,0,240])
RED_HIGH_HSV = np.array([30,30,255])

MIN_CONTOUR_AREA = 5
MAX_CONTOUR_AREA = 250



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


algorithms.largestArea = 0
algorithms.minPtsDistance = sys.float_info.max

contours = cvUtil.getContoursForColor(ledImage,selectLowHSV,selectHighHSV,MIN_CONTOUR_AREA,MAX_CONTOUR_AREA)
centerLst = algorithms.removeCloseContours(contours,20)
closestCenters = algorithms.getNClosestPoints(centerLst,4)

lrgTriPtList = algorithms.getLargestTriangle(closestCenters)
baseCenterPt = algorithms.getClosestPt(lrgTriPtList,closestCenters)
sortedPts = algorithms.getSortedPtListInTri(baseCenterPt,lrgTriPtList)
drawDirectionalTriangle(ledImage,sortedPts)


cv2.namedWindow('ledImage')
cv2.setMouseCallback('ledImage',fc.frameClickEvent,ledImage)

while(True):
	cv2.imshow('ledImage',ledImage)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break