#!/usr/bin/env python

'''
Simple "Square Detector" program.

Loads several images sequentially and tries to find squares in each image.
'''

import numpy as np
import cv2
#from color_blob_detection import getHSVChannel

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []

    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hChannelImg = imgHSV[:,:,0]
    sChannelImg = imgHSV[:,:,1]

    blurredHImg = cv2.GaussianBlur(hChannelImg,(11,11),0,0)
    blurredSImg = cv2.GaussianBlur(sChannelImg,(11,11),0,0)
    hThreshImg = cv2.inRange(blurredHImg,0,10)
    sThreshImg = cv2.inRange(blurredSImg,155,255)
    combImg = cv2.bitwise_and(hThreshImg,sThreshImg)

    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                #finds the edges os the square using canny and dilate
                bin = cv2.Canny(gray, 0, 20, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

if __name__ == '__main__':
    """from glob import glob
    for fn in glob('../cpp/pic*.png'):
        img = cv2.imread(fn)
        squares = find_squares(img)
        cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
        cv2.imshow('squares', img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break"""
    videoCap = cv2.VideoCapture(0)
    videoCap.set(3,640)
    videoCap.set(4,480)

    if(videoCap.isOpened() != True):
	    videoCap.open()

    while(True):
        ret,img = videoCap.read()
        squares = find_squares(img)
        cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
        cv2.imshow('squares', img)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    videoCap.release()
    cv2.destroyAllWindows()
