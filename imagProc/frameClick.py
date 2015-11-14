
import cv2
import numpy as np

def convertRGBColorToHSV(colorScalar):
	rgb_img = np.zeros((1,1,3),np.uint8)
	rgb_img[0,0] = colorScalar
	hsv_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
	return hsv_img[0,0]

def getSubArray(arr,size,x,y):
	nrd = arr.shape
	numRows = nrd[0]
	numCols = nrd[1]

	halfSize = size/2
	startY = y - halfSize if y - halfSize >= 0 else 0
	endY = y + halfSize if y + halfSize < numRows else numRows
	startX = x - halfSize if x - halfSize >= 0 else 0
	endX = x + halfSize if x + halfSize < numCols else numCols

	subArr = np.empty([(endY-startY)+1,(endX-startX)+1,3])

	for cRow in range(startY,endY+1):
		for cCol in range(startX, endX+1):
			subArr[cRow-startY][cCol-startX] = arr[cRow][cCol]
	return subArr

def frameClickEvent(event,x,y,flags,frame):
	if event == cv2.EVENT_LBUTTONUP:
		blurredFrame = cv2.GaussianBlur(frame,(5,5),0,0)
		subFrame = getSubArray(blurredFrame,3,x,y)
		shape = subFrame.shape
		numRows = shape[0]
		numCols = shape[1]
		totSize = numRows * numCols
		# order is bgr
		avgBlue = np.sum(subFrame[:,:,0])/totSize
		avgGreen = np.sum(subFrame[:,:,1])/totSize
		avgRed = np.sum(subFrame[:,:,2])/totSize

		avgColor = np.array([avgBlue,avgGreen,avgRed])
		avgHSVColor = convertRGBColorToHSV(avgColor)
		print avgHSVColor