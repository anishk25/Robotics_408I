__author__ = 'Durin'
#! /usr/bin/env python

import cv2
import numpy

color_tracker_window = "Color Tracker"

class ColorTracker:

    def __init__(self):
        cv2.cv.NamedWindow( color_tracker_window, 1 )
        self.capture = cv2.cv.CaptureFromCAM(0)

    def run(self):
        while True:
            img = cv2.cv.QueryFrame( self.capture )
            #test_img = cv2.imread(img)

            #blur the source image to reduce color noise
            #cv2.cv.Smooth(img, img, cv2.cv.CV_BLUR, 3)
            #cv2.GaussianBlur(test_img, 3, 0, img, 0, cv2.BORDER_DEFAULT)

            #convert the image to hsv(Hue, Saturation, Value) so its
            #easier to determine the color to track(hue)
            hsv_img = cv2.cv.CreateImage(cv2.cv.GetSize(img), 8, 3)
            cv2.cv.CvtColor(img, hsv_img, cv2.cv.CV_BGR2HSV)


            #limit all pixels that don't match our criteria, in this case we are
            #looking for purple but if you want you can adjust the first value in
            #both turples which is the hue range(120,140).  OpenCV uses 0-180 as
            #a hue range for the HSV color model
            thresholded_img =  cv2.cv.CreateImage(cv2.cv.GetSize(hsv_img), 8, 1)

            print thresholded_img

            #blue
            #cv2.cv.InRangeS(hsv_img, (110, 80, 80), (130, 240, 240), thresholded_img)
            #orange
            cv2.cv.InRangeS(hsv_img, (5,250,50), (15, 255, 255),thresholded_img)


            #determine the objects moments and check that the area is large
            #enough to be our object
            matmat = cv2.cv.GetMat(thresholded_img)
            moments = cv2.cv.Moments(matmat, 0)
            area = cv2.cv.GetCentralMoment(moments, 0, 0)


            #there can be noise in the video so ignore objects with small areas
            if(area > 200000):
                #determine the x and y coordinates of the center of the object
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area
                x = int(cv2.cv.GetSpatialMoment(moments, 1, 0)/area)
                y = int(cv2.cv.GetSpatialMoment(moments, 0, 1)/area)

                #print 'x: ' + str(x) + ' y: ' + str(y) + ' area: ' + str(area)

                #create an overlay to mark the center of the tracked object
                overlay = cv2.cv.CreateImage(cv2.cv.GetSize(img), 8, 3)

                cv2.cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20)
                cv2.cv.Add(img, overlay, img)
                #add the thresholded image back to the img so we can see what was
                #left after it was applied
                cv2.cv.Merge(thresholded_img, None, None, None, img)
                print "X: "+str(x)+"    Y: "+str(480-y)


            #display the image
            cv2.cv.ShowImage(color_tracker_window, img)

            if cv2.cv.WaitKey(10) == 27:
                break

if __name__=="__main__":
    color_tracker = ColorTracker()
    color_tracker.run()
