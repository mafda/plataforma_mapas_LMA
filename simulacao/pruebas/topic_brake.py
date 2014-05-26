#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

pub = rospy.Publisher('mi_carrito/brake_pedal/cmd', Float64)
#pub = rospy.Publisher('vilma_vehicle/brake_pedal/cmd', Float64)
rospy.init_node('brake_pedal')

# while not rospy.is_shutdown():
pub.publish(Float64(0.0))
rospy.sleep(1.0)