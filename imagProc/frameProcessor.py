import cv2
import numpy as np
import cv_utility as cvUtil
import algorithms

class FrameProcessor:

	ORANGE_LOW_HSV = np.array([0,100,200])
	ORANGE_HIGH_HSV = np.array([20,160,255])
	BLUE_LOW_HSV = np.array([95,215,215])
	BLUE_HIGH_HSV = np.array([105,235,235])

	CONE_MIN_AREA = 100
	CONE_MAX_AREA = 300
	LEDS_MIN_AREA = 1
	LEDS_MAX_AREA = 50
	
	def __init__(self):
		self.__robotAngle = 0

	def getRobotAngle(self):
		return self.__robotAngle

	def processFrame(self,frame):
		coneCenter = self.getConeCenterPoint(frame)
		# this list is sorted meaning, the last value in list is the top point of the triangle
		# and the other two are bottom points
		triangleLst = getTrianglePointLst(frame)
		# CALCULATE ROBOT HEADING HERE!!!!!!

	def getConeCenterPoint(self,frame):
		o_contours = cvUtil.getContoursForColor(frame,FrameProcessor.ORANGE_LOW_HSV,FrameProcessor.ORANGE_HIGH_HSV,
												FrameProcessor.CONE_MIN_AREA,FrameProcessor.CONE_MAX_AREA)
		cvUtil.sortContoursByArea(o_contours)
		centerLst = cvUtil.getCenterOfContours(o_contours)
		if(len(centerLst) >= 1):
			return centerLst[0]
		else:
			return None

	def getTrianglePointLst(self,frame):
		algorithms.largestArea = 0
		algorithms.minPtsDistance = sys.float_info.max
		contours = cvUtil.getContoursForColor(frame,FrameProcessor.BLUE_LOW_HSV,FrameProcessor.BLUE_HIGH_HSV,
													FrameProcessor.LEDS_MIN_AREA,FrameProcessor.LEDS_MAX_AREA)
		centerLst = algorithms.removeCloseContours(contours,10)
		closestCenters = algorithms.getNClosestPoints(centerLst,4)
		if(closestCenters != None):
			lrgTriPtList = algorithms.getLargestTriangle(closestCenters)
			baseCenterPt = algorithms.getClosestPt(lrgTriPtList,closestCenters)
			sortedPts = algorithms.getSortedPtListInTri(baseCenterPt,lrgTriPtList)
			return sortedPts
		else:
			return None




	


