#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

pub = rospy.Publisher('mi_carrito/gas_pedal/cmd', Float64)
#pub = rospy.Publisher('vilma_vehicle/gas_pedal/cmd', Float64)
rospy.init_node('gas_pedal')

# while not rospy.is_shutdown():

x = 0.0
for i in range(11):	
	pub.publish(Float64(x))
	rospy.sleep(0.1)
	x = x + 0.1