#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib
import sys
import rospy
import cv
from math import sin, cos, sqrt, pi
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

red_lower = (178, 218, 57) #color minimo vermelho
red_upper = (179, 232, 64) #color maximo vermelho

font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8) #fonte da tipografia para o texto da distancia

class ColorTracker:

    def __init__(self):
        rospy.init_node('detection_vilma_camera') #hjh

        self.cv_window_name = "Detection Vilma Camera" # Nome da janela
        cv.NamedWindow(self.cv_window_name, 0) # Cria uma janela re-sizeable (segundo parametro = 0)

        self.bridge = CvBridge() # Cria um objeto cv_bridge

        self.image_sub = rospy.Subscriber("/Vilma_Car/Vilma_Camera/Vilma_Camera", Image, self.callback) #Subscribe o topic da imagen da camera
       
    def callback(self, data):
        try:
            img = self.bridge.imgmsg_to_cv(data, "bgr8") #Converte a imagem para o formato OpenCV
        except CvBridgeError, e:
            print e

        cv.Smooth(img, img, cv.CV_BLUR, 3) #; desfocar a imagem de origem para reduzir o ruido da cor

        hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3) #convert the image to hsv(Hue, Saturation, Value) so its  easier to determine the color to track(hue) 
        cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

        #limit all pixels that don't match our criteria, in this case we are  
        #looking for purple but if you want you can adjust the first value in  
        #both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
        #a hue range for the HSV color model 
        thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        cv.InRangeS(hsv_img, red_lower, red_upper, thresholded_img)

        moments = cv.Moments(cv.GetMat(thresholded_img), 0) #determine the objects moments and check that the area is large  enough to be our object 
        area = cv.GetCentralMoment(moments, 0, 0)

        #there can be noise in the video so ignore objects with small areas 
        if(area > 100000):
            #determine the x and y coordinates of the center of the object 
            #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
            x = cv.GetSpatialMoment(moments, 1, 0)/area
            y = cv.GetSpatialMoment(moments, 0, 1)/area
            
            cv.Circle(img, (int(x),int(y)), 2, (255, 0, 0), 20)

        cv.ShowImage(self.cv_window_name, img) #Refresh the image on the screen
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