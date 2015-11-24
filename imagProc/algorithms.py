import cv2
import cv_utility as cvUtil
import operator
import math
import sys

largestArea = 0
minPtsDistance = sys.float_info.max

def getAreaOfCircle(radius):
	return math.pi * (radius**2)

# gets the distance between two points
def getDist(pt1,pt2):
	n1 = (pt2[1] - pt1[1])**2
	n2 = (pt2[0] - pt1[0])**2
	return math.sqrt(n1 + n2)
	

# gets the distance between a line and a point
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

# gets the area of a triangle
def getAreaOfTriangle(triPts):
	assert(len(triPts) == 3)
	n1 = triPts[0][0]*(triPts[1][1] - triPts[2][1])
	n2 = triPts[1][0]*(triPts[2][1] - triPts[0][1])
	n3 = triPts[2][0]*(triPts[0][1] - triPts[1][1])
	area = abs(n1+n2+n3)/2
	return area

# gets the closest point to a triangle given a set of points
def getClosestPt(triPts, allPts):
	assert(len(triPts) == 3 and len(allPts) >= 3)
	allPtsLen = len(allPts)
	pt1 = triPts[0]
	pt2 = triPts[1]
	minDist = sys.float_info.max
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

# gets the largest triangle in a given set of points
def getLargestTriangle(allPointsList):
	trianglePtList = []
	lrgTriPtList = []
	largestTriangleHelper(allPointsList,trianglePtList,lrgTriPtList,0,0)
	return lrgTriPtList

# sorts the points in the triangle based on the distance from the base point
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

# removes contours that are close to each other
# given the min distance needed between each contour
# returns the list of center points for the contours
def removeCloseContours(contours,minDist):
	removeIndices = []
	centerLst = cvUtil.getCenterOfContours(contours)
	contoursLen = len(contours)
	for i in range(0,contoursLen):
		area_i = cv2.contourArea(contours[i])
		if(centerLst[i][0] >= 0):
			for j in range(i+1,contoursLen):
				area_j = cv2.contourArea(contours[j])
				if(centerLst[i][0] >= 0 and centerLst[j][0] >= 0):
					dist = getDist(centerLst[i],centerLst[j])
					if(dist < minDist):
						if(area_j < area_i):
							centerLst[j] = (-1,-1)
							removeIndices.append(j)
						else:
							centerLst[i] = (-1,-1)
							removeIndices.append(i)
							break

	for index in sorted(removeIndices, reverse=True):
		del centerLst[index]
		del contours[index]
	return centerLst

def sumUpAllDistances(points):
	ptsLen = len(points)
	dist = 0
	for i in range(0,ptsLen):
		for j in range(i+1,ptsLen):
			dist += getDist(points[i],points[j])
	return dist

def closestPointHelper(allPointsList,currPointList,closestPtsList,currIndex,numPtsCovered,N):
	if(numPtsCovered < N):
		for i in range(currIndex,len(allPointsList)):
			currPointList.append(allPointsList[i])
			closestPointHelper(allPointsList,currPointList,closestPtsList,i+1,numPtsCovered+1,N)
			currPointList.pop()
	else:
		global minPtsDistance
		sumDists = sumUpAllDistances(currPointList)
		if(sumDists < minPtsDistance):
			minPtsDistance = sumDists
			del closestPtsList[:]
			closestPtsList.extend(currPointList)

def getNClosestPoints(points,N):
	ptsLen = len(points)
	if(ptsLen < N):
		return None
	currPointList = []
	closestPtsList = []
	closestPointHelper(points,currPointList,closestPtsList,0,0,N)
	return closestPtsList
