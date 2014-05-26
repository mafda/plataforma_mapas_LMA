#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray

robot_position = 1; #robot position in ModelStates array
pub = rospy.Publisher('vilma_linear_velocity', Float32MultiArray) #publicar a posicao
array = [0]*3;

def callback(data):
    Vx = data.twist[robot_position].linear.x
    Vy = data.twist[robot_position].linear.y
    Vz = data.twist[robot_position].linear.z
    Wx = data.twist[robot_position].angular.x
    Wy = data.twist[robot_position].angular.y
    Wz = data.twist[robot_position].angular.z
    
    print "velocidad:", Vx, Vy, Vz
    #print "angular:", Wx, Wy, Wz
    array = Float32MultiArray()
    array.data = [Vx, Vy, Vz]
    pub.publish(array)
   
def getModelStates():
    rospy.init_node('vilma_velocity', anonymous=True) #nome do nodo
    rospy.Subscriber("/gazebo/model_states", ModelStates, callback)
    rospy.spin()

if __name__ == '__main__':
    getModelStates()