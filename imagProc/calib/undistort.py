import numpy as np
import cv2

# copy parameters to arrays



K = np.array([[309.90883833,0.,329.08912208], [0.,309.2342956,212.92637703], [0, 0, 1]])
d = np.array([-0.04842532,0.07125209,-0.00571774,-0.00174375,0.2432097]) # just use first two terms (no translation)

# read one of your images
img = cv2.imread("calPics/cal_pic4.jpg")
h, w = img.shape[:2]

# undistort
newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0) 
newimg = cv2.undistort(img, K, d, None, newcamera)

cv2.imwrite("original.jpg", img)
cv2.imwrite("undistorted.jpg", newimg)