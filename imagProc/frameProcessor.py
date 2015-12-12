import cv2
import numpy as np
import cv_utility as cvUtil
import algorithms
import sys

class FrameProcessor:

	ORANGE_LOW_HSV = np.array([0,130,200])
	ORANGE_HIGH_HSV = np.array([20,160,255])
	BLUE_LOW_HSV = np.array([90,150,242])
	BLUE_HIGH_HSV = np.array([100,210,255])

	CONE_MIN_AREA = 100
	CONE_MAX_AREA = 500
	LEDS_MIN_AREA = 1
	LEDS_MAX_AREA = 200

	LED_KERNEL = np.ones((3,3),np.uint8)
	CONE_KERNEL = np.ones((5,5),np.uint8)
	
	def __init__(self):
		self.__coneCenter = (0,0)
		self.__triangleTopPt = (0,0)
		self.__triangleBaseCenterPt = (0,0)

	def getRobotAngle(self):
		return self.__robotAngle

	def processFrame(self,frame):
		cent = self.getConeCenterPoint(frame)
		if(cent == None):
			self.__coneCenter = (-1,-1)
		else:
			self.__coneCenter = cent
		# this list is sorted meaning, the last value in list is the top point of the triangle
		# and the other two are bottom points
		baseCenterPt,triangleLst = self.getTrianglePointLst(frame)
		if(triangleLst == None):
			self.__triangleBaseCenterPt = (-1,-1)
			self.__triangleTopPt = (-1,-1)
		else:
			self.__triangleBaseCenterPt = baseCenterPt
			self.__triangleTopPt = triangleLst[2]

		# CALCULATE ROBOT HEADING HERE!!!!!!

	def getConeCenterPoint(self,frame):
		o_contours = cvUtil.getContoursForColor(frame,FrameProcessor.ORANGE_LOW_HSV,FrameProcessor.ORANGE_HIGH_HSV,
												FrameProcessor.CONE_MIN_AREA,FrameProcessor.CONE_MAX_AREA,FrameProcessor.CONE_KERNEL)
		if(len(o_contours) > 0):
			lrgContour = cvUtil.getLargestContour(o_contours)
			centerLst = cvUtil.getCenterOfContours([lrgContour])
			cvUtil.drawCircleForPoints(frame,centerLst,3,(0,255,0),3)
			return centerLst[0]
		return None

	def getTrianglePointLst(self,frame):
		algorithms.largestArea = 0
		algorithms.minPtsDistance = sys.float_info.max

		contours = cvUtil.getContoursForColor(frame,FrameProcessor.BLUE_LOW_HSV,FrameProcessor.BLUE_HIGH_HSV,
													FrameProcessor.LEDS_MIN_AREA,FrameProcessor.LEDS_MAX_AREA,FrameProcessor.LED_KERNEL)
		centerLst = algorithms.removeCloseContours(contours,2)
		closestCenters = algorithms.getNClosestPoints(centerLst,4)

		if(closestCenters != None):
			#cvUtil.drawCircleForPoints(frame,closestCenters,5,(0,0,255),1)
			lrgTriPtList = algorithms.getLargestTriangle(closestCenters)
			baseCenterPt = algorithms.getClosestPt(lrgTriPtList,closestCenters)
			sortedPts = algorithms.getSortedPtListInTri(baseCenterPt,lrgTriPtList)
			cvUtil.drawDirectionalTriangle(frame,sortedPts)
			return baseCenterPt,sortedPts
		else:
			return None,None

	def getRobotVector(self):
		if(self.__triangleBaseCenterPt[0] == -1):
			return None
		return (self.__triangleTopPt[0] - self.__triangleBaseCenterPt[0],(self.__triangleTopPt[1] - self.__triangleBaseCenterPt[1])*-1)

	def getConeVector(self):
		if(self.__triangleBaseCenterPt[0] == -1 or self.__coneCenter[0] == -1):
			return None

		midPt = ((self.__triangleTopPt[0] + self.__triangleBaseCenterPt[0])/2,
				 (self.__triangleTopPt[1] + self.__triangleBaseCenterPt[1])/2)
		#midPt = self.__triangleTopPt
		return (self.__coneCenter[0]-midPt[0], (self.__coneCenter[1]-midPt[1])*-1)


	def getRobotPosition(self):
		if(self.__triangleBaseCenterPt[0] == -1):
			return None
		midPt = ((self.__triangleTopPt[0] + self.__triangleBaseCenterPt[0])/2,
				 (self.__triangleTopPt[1] + self.__triangleBaseCenterPt[1])/2)
		return midPt