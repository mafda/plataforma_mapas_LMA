#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib
import sys
import rospy
import cv
from math import sin, cos, sqrt, pi
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge, CvBridgeError

pub = rospy.Publisher('position_obj_R', Float32MultiArray) #publicar o topico

horizontal_samples = 64 #samples scan horizontal para a matriz
vertical_samples = 48 #samples scan vertical para a matriz

xo = [[0 for x in xrange(horizontal_samples)] for x in xrange(vertical_samples)] #matriz do tamanho samples horinzontal e vertical
yo = [[0 for x in xrange(horizontal_samples)] for x in xrange(vertical_samples)] #matriz do tamanho samples horinzontal e vertical
zo = [[0 for x in xrange(horizontal_samples)] for x in xrange(vertical_samples)] #matriz do tamanho samples horinzontal e vertical
d = [[0 for x in xrange(horizontal_samples)] for x in xrange(vertical_samples)] #matriz do tamanho samples horinzontal e vertical

red_lower = (178, 218, 57) #color minimo vermelho
red_upper = (179, 232, 64) #color maximo vermelho

font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8) #fonte da tipografia para o texto da distancia

class ColorTracker:

    def __init__(self):
        rospy.init_node('detection_vilma_camera_scan') #Nome do nodo

        self.cv_window_name = "Detection Vilma Camera" # Nome da janela
        cv.NamedWindow(self.cv_window_name, 0) # Cria uma janela re-sizeable (segundo parametro = 0)

        self.bridge = CvBridge() # Cria um objeto cv_bridge opencv

        self.image_sub = rospy.Subscriber("/Vilma_Car/Vilma_Camera/Vilma_Camera", Image, self.callback) #Subscribe o topic da imagen da camera
        self.velodyne_sub =  rospy.Subscriber("scan", PointCloud, self.callback_velodyne) #Subscribe o topic do laser scan

    def callback_velodyne(self, data): # determinar a distancia da camera ao objeto
        for j in range(vertical_samples): # de 0 a 47, vertical 48
            for i in range(horizontal_samples-1,-1,-1): # 63 a 0, horizontal 64

                X = data.points[(j*horizontal_samples)+i].x  # posicao em x da matriz ij=(i,j)
                Y = data.points[(j*horizontal_samples)+i].y  # posicao em y da matriz ij=(i,j)
                Z = data.points[(j*horizontal_samples)+i].z  # posicao em z da matriz ij=(i,j)

                global xo,yo,zo,d

                xo[j][horizontal_samples-1-i] = X  # coordenada em x da matriz (i,j)=ij
                yo[j][horizontal_samples-1-i] = Y  # coordenada em y da matriz (i,j)=ij
                zo[j][horizontal_samples-1-i] = Z  # coordenada em z da matriz (i,j)=ij
                d[j][horizontal_samples-1-i] = sqrt(X*X+ Y*Y+Z*Z) #matriz que determina a distancia da camera ao objeto


    def callback_velodyne(self, data):
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
        if(area > 5000):
            #determine the x and y coordinates of the center of the object
            #we are tracking by dividing the 1, 0 and 0, 1 moments by the area
            x = cv.GetSpatialMoment(moments, 1, 0)/area
            y = cv.GetSpatialMoment(moments, 0, 1)/area
            x = int(x)
            y = int(y)

            area = area / 100 #area do circulo
            r = sqrt(area / pi) #area do circulo
            r = int(r)
            cv.Circle(img, (x,y), r, (0, 255, 0), 2) #desenha o circulo

            s = cv.GetSize(img) #obter o tamanho da janela
            width = s[0] #largura da janela
            height = s[1] #alto da janela

            p1 = (x, 0) #ponto 1 para a linha vertical
            p2 = (x, height) #ponto 2 para a linha vertical
            cv.Line(img, p1, p2,  (0, 255, 0), 2) #desenha a linha vertical
            p1 = (0, y) #ponto 1 para a linha horizontal
            p2 = (width, y) #ponto 2 para a linha horizontal
            cv.Line(img, p1, p2,  (0, 255, 0), 2) #desenha a linha horizontal

            i = int(round(horizontal_samples * (x*1.0 / width))) #fefw
            j = int(round(vertical_samples * (y*1.0 / height))) #efw
            #print i,j
            cv.PutText(img,str(d[j][i]), (x+r,y+r),font, (55,25,255)) #Por o texto da distancia da camera ao objeto
            array = Float32MultiArray()
            array.data = [xo[j][i], yo[j][i], zo[j][i], d[j][i],1]
            pub.publish(array)
            print xo[j][i], yo[j][i], zo[j][i], d[j][i]

        else:
            array = Float32MultiArray()
            array.data = [-1, -1, -1, -1, 0]
            pub.publish(array)
            
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
