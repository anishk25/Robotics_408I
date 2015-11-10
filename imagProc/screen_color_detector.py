import numpy as np
import cv2
import math

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4 

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

frame = None


def convertRGBColorToHSV(colorScalar):
	rgb_img = np.zeros((1,1,3),np.uint8)
	rgb_img[0,0] = colorScalar
	hsv_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
	print hsv_img[0,0]
	return hsv_img[0,0]

#center sub array around x and y
#size is the size of the square
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


def frameClickEvent(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONUP:
		subFrame = getSubArray(frame,4,x,y)
		shape = subFrame.shape
		numRows = shape[0]
		numCols = shape[1]
		totSize = numRows * numCols
		# order is bgr
		avgBlue = np.sum(subFrame[:,:,0])/totSize
		avgGreen = np.sum(subFrame[:,:,1])/totSize
		avgRed = np.sum(subFrame[:,:,2])/totSize

		avgColor = np.array([avgBlue,avgRed,avgGreen])
		avgHSVColor = convertRGBColorToHSV(avgColor)
		print avgHSVColor


videoCap = cv2.VideoCapture(0)
videoCap.set(CV_CAP_PROP_FRAME_WIDTH,640)
videoCap.set(CV_CAP_PROP_FRAME_HEIGHT,480)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame',frameClickEvent)

if(videoCap.isOpened() != True):
	videoCap.open()

while(True):
	ret,frame = videoCap.read()
	cv2.imshow('frame',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break


videoCap.release()
cv2.destroyAllWindows()

