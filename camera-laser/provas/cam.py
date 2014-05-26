#!/usr/bin/env python

import roslib
import sys
import rospy
import cv
from math import sin, cos, sqrt, pi
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

USE_STANDARD = False

# red_lower = (55, 0, 55)
# red_upper = (5, 255, 255)
red_lower = (178, 218, 57)
red_upper = (179, 232, 64)

import time
x_co = 0
y_co = 0
def on_mouse(event,x,y,flag,param):
    global x_co
    global y_co
    if(event==cv.CV_EVENT_MOUSEMOVE):
        x_co=x
        y_co=y

class ColorTracker:

    def __init__(self):
        rospy.init_node('detection_vilma_camera')

        """ Give the OpenCV display window a name. """
        self.cv_window_name = "Detection Vilma Camera"
        #self.cv_window_name1 = "Debug"

        """ Create the window and make it re-sizeable (second parameter = 0) """
        cv.NamedWindow(self.cv_window_name, 0)
        #cv.NamedWindow(self.cv_window_name1, 0)

        """ Create the cv_bridge object """
        self.bridge = CvBridge()

        """ Subscribe to the camera image topic """
        self.image_sub = rospy.Subscriber("/Vilma_Car/Vilma_Camera/Vilma_Camera", Image, self.callback)

    def callback(self, data):
        try:
            """ Convert the image to OpenCV format """
            img = self.bridge.imgmsg_to_cv(data, "bgr8")
        except CvBridgeError, e:
            print e

        # font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)

        # cv.Smooth(src, src, cv.CV_BLUR, 3)
        # hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
        # thr = cv.CreateImage(cv.GetSize(src), 8, 1)
        # cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
        # cv.SetMouseCallback("camera",on_mouse, 0);
        # s=cv.Get2D(hsv,y_co,x_co)
        # print "H:",s[0],"      S:",s[1],"       V:",s[2]
        # cv.PutText(src,str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co),font, (55,25,255))
        # cv.ShowImage("camera", src)

        #blur the source image to reduce color noise 
        cv.Smooth(img, img, cv.CV_BLUR, 3);

        #convert the image to hsv(Hue, Saturation, Value) so its  
        #easier to determine the color to track(hue) 
        hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

        #limit all pixels that don't match our criteria, in this case we are  
        #looking for purple but if you want you can adjust the first value in  
        #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
        #a hue range for the HSV color model 
        thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        cv.InRangeS(hsv_img, red_lower, red_upper, thresholded_img)
        #cv.ShowImage(self.cv_window_name1, thresholded_img)

        #determine the objects moments and check that the area is large  
        #enough to be our object 
        moments = cv.Moments(cv.GetMat(thresholded_img), 0)
        area = cv.GetCentralMoment(moments, 0, 0)

        #create an overlay to mark the center of the tracked object 
        #overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
        #cv.Add(img, overlay, img)
        #add the thresholded image back to the img so we can see what was  
        #left after it was applied 
        #cv.Merge(thresholded_img, None, None, None,img)

        #there can be noise in the video so ignore objects with small areas 
        if(area > 100000):
            #determine the x and y coordinates of the center of the object 
            #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
            x = cv.GetSpatialMoment(moments, 1, 0)/area
            y = cv.GetSpatialMoment(moments, 0, 1)/area

            x = int(x)
            y = int(y)
            area = area / 100
            r = sqrt(area / pi)
            r = int(r)
            #print 'x: ' + str(x) + ' y: ' + str(y) + ' area: ' + str(area) 
            cv.Circle(img, (x,y), r, (255, 0, 0), 1)

            s = cv.GetSize(img)
            width = s[0]
            height = s[1]
            #print width, height

            p1 = (x, 0)
            p2 = (x, height)

            cv.Line(img, p1, p2,  (255, 0, 0), 1)

            p1 = (0, y)
            p2 = (width, y)

            cv.Line(img, p1, p2,  (255, 0, 0), 1)
  
        """ Refresh the image on the screen """
        cv.ShowImage(self.cv_window_name, img)
        cv.WaitKey(3)

def main(args):
    vn = ColorTracker()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vison node."
    cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)