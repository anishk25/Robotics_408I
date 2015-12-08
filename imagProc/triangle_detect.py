import cv2
import numpy as np
import frameClick as fc
import cv_utility as cvUtil
import algorithms
import sys

BLUE_LOW_HSV = np.array([95,215,215])
BLUE_HIGH_HSV = np.array([105,235,235])

YELLOW_LOW_HSV = np.array([35,0,240])
YELLOW_HIGH_HSV = np.array([45,10,255])

PURPLE_LOW_HSV = np.array([130,0,240])
PURPLE_HIGH_HSV = np.array([160,25,255])

RED_LOW_HSV = np.array([10,40,220])
RED_HIGH_HSV = np.array([20,70,255])

ORANGE_LOW_HSV = np.array([0,100,200])
ORANGE_HIGH_HSV = np.array([20,160,255])


CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 
CV_CAP_PROP_CONTRAST = 11

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

MIN_CONTOUR_AREA = 1
MAX_CONTOUR_AREA = 250




def drawDirectionalTriangle(img,sortedTriPts):
	 assert(len(sortedTriPts) == 3)
	 # draw green line at base
	 cv2.line(img,sortedPts[0],sortedPts[1],(0,255,0),2)
	 # draw red line for other two sides
	 cv2.line(img,sortedPts[0],sortedPts[2],(0,0,255),2)
	 cv2.line(img,sortedPts[1],sortedPts[2],(0,0,255),2)


selectLowHSV = BLUE_LOW_HSV
selectHighHSV = BLUE_HIGH_HSV

videoCap = cv2.VideoCapture(0)
videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)

kernel = np.ones((2,2),np.uint8)

while(True):
	ret,frame = videoCap.read()
	cv2.setMouseCallback('frame',fc.frameClickEvent,frame)
	#hsvFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	#threshImg = cv2.inRange(hsvFrame,selectLowHSV,selectHighHSV)
	#erodedDilImg = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, kernel)

	
	'''
	algorithms.largestArea = 0
	algorithms.minPtsDistance = sys.float_info.max
	contours = cvUtil.getContoursForColor(frame,selectLowHSV,selectHighHSV,MIN_CONTOUR_AREA,MAX_CONTOUR_AREA,True)
	centerLst = algorithms.removeCloseContours(contours,10)
	cvUtil.drawCircleForPoints(frame,centerLst,5,(0,255,0),1)
	print centerLst
	#closestCenters = algorithms.getNClosestPoints(centerLst,4)
	#cvUtil.drawCircleForPoints(frame,closestCenters,5,(0,255,0),1)
	'''
	
	'''
	if(closestCenters == None):
		cv2.imshow('frame',frame)
		continue

	lrgTriPtList = algorithms.getLargestTriangle(closestCenters)
	baseCenterPt = algorithms.getClosestPt(lrgTriPtList,closestCenters)
	sortedPts = algorithms.getSortedPtListInTri(baseCenterPt,lrgTriPtList)
	drawDirectionalTriangle(frame,sortedPts)
	
	
	#cvUtil.drawCircleForPoints(frame,closestCenters,10,(0,255,0),2)
	'''


	#cv2.imshow('frame',threshImg)
	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break
	



'''
contours = cvUtil.getContoursForColor(ledImage,selectLowHSV,selectHighHSV,MIN_CONTOUR_AREA,MAX_CONTOUR_AREA)
centerLst = algorithms.removeCloseContours(contours,20)
closestCenters = algorithms.getNClosestPoints(centerLst,4)
lrgTriPtList = algorithms.getLargestTriangle(closestCenters)
baseCenterPt = algorithms.getClosestPt(lrgTriPtList,closestCenters)
sortedPts = algorithms.getSortedPtListInTri(baseCenterPt,lrgTriPtList)
drawDirectionalTriangle(ledImage,sortedPts)
'''
