#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

pub = rospy.Publisher('mi_carrito/hand_brake/cmd', Float64)
#pub = rospy.Publisher('vilma_vehicle/hand_brake/cmd', Float64)
rospy.init_node('hand_brake')

x = 1.0
for i in range(11):	
	pub.publish(Float64(x))
	rospy.sleep(0.1)
	x = x - 0.1

# while not rospy.is_shutdown():
	# pub.publish(Float64(0.0))
	# rospy.sleep(1.0)