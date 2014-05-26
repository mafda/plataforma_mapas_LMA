#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
import math

# Car position - car to origin
Xcar_o = 0
Ycar_o = 0
Theta_car = 0

# Cam position - cam to car (model.sdf  <pose>1.2 0.0 1.1 0 0 0</pose>)
Xcam_car = 1.2
Ycam_car = 0.0

# obj position - obj to cam
Xr_cam = 0
Yr_cam = 0
obj_in_scene = 0

def callbackCarPos(data):
    global Xcar_o, Ycar_o, Theta_car
    Xcar_o = data.data[0]
    Ycar_o = data.data[1]
    Theta_car = data.data[5]

def callbackObjPos(data):
    global Xr_cam, Yr_cam, obj_in_scene
    Xr_cam = data.data[0]
    Yr_cam = data.data[1]
    obj_in_scene = data.data[4]
    
if __name__ == '__main__':
    rospy.init_node('abs_obs_pos', anonymous=True)

    rospy.Subscriber("car_position_euler", Float32MultiArray, callbackCarPos)
    rospy.Subscriber("obj_position", Float32MultiArray, callbackObjPos)

    pub = rospy.Publisher('abs_obs_pos', Float32MultiArray)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    r = rospy.Rate(5)
    counter = 0
    Xr_o_accum = 0
    Yr_o_accum = 0
    while not rospy.is_shutdown():
        if obj_in_scene:
            print "car_o: ", Xcar_o, Ycar_o, Theta_car
            print "cam_car: ", Xcam_car, Ycam_car
            print "R_cam: ", Xr_cam, Yr_cam 

            a1 = math.cos(Theta_car) 
            a2 = math.sin(Theta_car)
            a3 = Xcam_car + Xr_cam
            a4 = Xcar_o
            b3 = Ycam_car + Yr_cam
            b4 = Ycar_o
            Xr_o = a1 * a3 + (-a2 * b3) + a4
            Yr_o = a2 * a3 + a1 * b3 + b4
            print Xr_o, Yr_o

            counter = counter + 1;
            Xr_o_accum = Xr_o_accum + Xr_o
            Yr_o_accum = Yr_o_accum + Yr_o
            
            Xr_o_mean = Xr_o_accum / counter
            Yr_o_mean = Yr_o_accum / counter

            # print Xr_o_mean, Yr_o_mean

            array = Float32MultiArray()
            array.data = [Xr_o_mean, Yr_o_mean,1]
            pub.publish(array)

        else:
            counter = 0;
            Xr_o_accum = 0
            Yr_o_accum = 0
            array = Float32MultiArray()
            array.data = [-1,-1,0]
            #print "Obj doesn't appear in the scene"
            pub.publish(array)

        r.sleep()
