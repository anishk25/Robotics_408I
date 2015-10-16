import numpy as np
import cv2
from PIL import Image

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 

COLOR_MIN = np.array([104, 178, 70 ])
COLOR_MAX = np.array([130, 240, 124 ])
MIN_CONTOUR_AREA = 50


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

videoCap = cv2.VideoCapture(0)
videoCap.set(CV_CAP_PROP_FRAME_WIDTH,640)
videoCap.set(CV_CAP_PROP_FRAME_HEIGHT,480)

if(videoCap.isOpened() != True):
	videoCap.open()

while(True):
	ret,frame = videoCap.read()
	imgThresh = getThresholdedImageHSV(frame)

	contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	fContours = filterContours(contours)

	cv2.drawContours(frame, fContours, -1, (0,255,0), 1)

	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

videoCap.release()
cv2.destroyAllWindows()