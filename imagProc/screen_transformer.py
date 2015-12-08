import numpy as np
import cv2

def order_points(pts):
	ordPoints = []

	'''
	y_max_in = np.argmax(pts[:,1])
	y_min_in = np.argmin(pts[:,1])
	x_max_in = np.argmax(pts[:,0])
	x_min_in = np.argmin(pts[:,0])

	ordPoints.append(tuple(pts[x_min_in]))
	ordPoints.append(tuple(pts[y_max_in]))
	ordPoints.append(tuple(pts[x_max_in]))
	ordPoints.append(tuple(pts[y_min_in]))
	'''

	for pt in pts:
		ordPoints.append(tuple(pt))
	return ordPoints

def drawRectOnFrame(frame,pts):
	if(len(pts) == 4):
		cv2.line(frame,pts[0],pts[3],(0,255,0),1)
		for i in range(0,len(pts)-1):
			cv2.line(frame,pts[i],pts[i+1],(0,255,0),1)

def getTransFormImage(img,cornersInImg,wantedCorners,size):
	if(cornersInImg != None):
		transmtx = cv2.getPerspectiveTransform(cornersInImg.astype(np.float32),wantedCorners.astype(np.float32))
		return cv2.warpPerspective(img,transmtx,size)
	else:
		return None
