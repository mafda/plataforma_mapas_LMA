#!/usr/bin/env python

import roslib
import sys
import rospy
import cv
from math import sin, cos, sqrt, pi
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

USE_STANDARD = False

class test_vision_node:

    def __init__(self):
        rospy.init_node('lane_marking_detection')

        """ Give the OpenCV display window a name. """
        self.cv_window_name = "cam_front/image"
        self.cv_window_name2 = "processed"

        """ Create the window and make it re-sizeable (second parameter = 0) """
        cv.NamedWindow(self.cv_window_name, 0)
        cv.NamedWindow(self.cv_window_name2, 0)

        """ Create the cv_bridge object """
        self.bridge = CvBridge()

        """ Subscribe to the camera image topic """
        self.image_sub = rospy.Subscriber("/cam_front/image", Image, self.callback)

    def callback(self, data):
        try:
            """ Convert the image to OpenCV format """
            cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
        except CvBridgeError, e:
          print e
  
        
        """ Get the width and height of the image """
        # (width, height) = cv.GetSize(cv_image)

        # """ Overlay some text onto the image display """
        # text_font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 2, 2)
        # cv.PutText(cv_image, "Maria Fernanda", (50, height / 2), text_font, cv.RGB(255, 255, 0))

        # gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # edges = cv2.Canny(gray, 80, 120)

        size = cv.GetSize(cv_image)
  
        # Create a gray scale image
        gray_image = cv.CreateImage(size, 8, 1)
        cv.CvtColor(cv_image, gray_image, cv.CV_RGB2GRAY)
      
        # Create an image to save edge data to
        edges_image = cv.CreateImage(size, 8, 1)
      
        # Canny edge detection
        # http://opencv.willowgarage.com/documentation/python/feature_detection.html
        cv.Canny(gray_image, edges_image, 50.0, 300.0)

        storage = cv.CreateMemStorage(0)
        lines = 0

        if USE_STANDARD:
            lines = cv.HoughLines2(edges_image, storage, cv.CV_HOUGH_STANDARD, 1, pi / 180, 100, 0, 0)
            for (rho, theta) in lines[:100]:
                a = cos(theta)
                b = sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
                pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
                cv.Line(cv_image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8)
        else:
            lines = cv.HoughLines2(edges_image, storage, cv.CV_HOUGH_PROBABILISTIC, 1, pi / 180, 50, 50, 10)
            for line in lines:
                cv.Line(cv_image, line[0], line[1], cv.CV_RGB(255, 0, 0), 3, 8)
  
        """ Refresh the image on the screen """
        cv.ShowImage(self.cv_window_name2, edges_image)
        cv.ShowImage(self.cv_window_name, cv_image)
        cv.WaitKey(3)

def main(args):
      vn = test_vision_node()
      try:
        rospy.spin()
      except KeyboardInterrupt:
        print "Shutting down vison node."
      cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)