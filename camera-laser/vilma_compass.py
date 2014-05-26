#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray
import math

robot_position = 1; #robot position in ModelStates array
pub = rospy.Publisher('compass_yaw', Float32MultiArray) #publicar a angulo do veiculo
array = [0]*3;

def callback(data):
    #obter a posicao 
    # x = data.pose[robot_position].position.x
    # y = data.pose[robot_position].position.y
    # z = data.pose[robot_position].position.z

    #obter a orientacao do veiculo 
    q0 = data.pose[robot_position].orientation.w
    q1 = data.pose[robot_position].orientation.x
    q2 = data.pose[robot_position].orientation.y
    q3 = data.pose[robot_position].orientation.z
    #print q0, q1, q2, q3
    #http://graphics.wikia.com/wiki/Conversion_between_quaternions_and_Euler_angles
    #http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles

    #converter a orientacao quaternion em orientacao em angulos roll, pitch, yaw do veiculo
    roll = math.atan((2*(q0*q1+q2*q3))/(1-2*(q1*q1+q2*q2)))
    pitch = math.asin(2*(q0*q2-q3*q1))
    yaw = math.atan(2*(q0*q3+q1*q2)/(1-2*(q2*q2+q3*q3)))

    #text ="FER roll = %f, pitch = %f, yaw = %f" % (roll, pitch, yaw)
    #print text

    array = Float32MultiArray()
    # array.data = [x, y, z, roll, pitch, yaw]
    array.data = [roll, pitch, yaw]
    pub.publish(array)

    #print roll, pitch, yaw
    #rospy.signal_shutdown('End of process!')

def getModelStates():
    rospy.init_node('quaternion2euler', anonymous=True) #nome do nodo
    rospy.Subscriber("/gazebo/model_states", ModelStates, callback)
    rospy.spin()

if __name__ == '__main__':
    getModelStates()