#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64


hand_brake = rospy.Publisher('mi_carrito/hand_brake/cmd', Float64)
gas_pedal = rospy.Publisher('mi_carrito/gas_pedal/cmd', Float64)
hand_wheel = rospy.Publisher('mi_carrito/hand_wheel/cmd', Float64)
brake_pedal = rospy.Publisher('mi_carrito/brake_pedal/cmd', Float64)


rospy.init_node('car_controller')

x = 1.0
for i in range(11):	
	hand_brake.publish(Float64(x))
	rospy.sleep(0.1)
	x = x - 0.1

rospy.sleep(1.0)

x = 0.0
for i in range(11):	
	gas_pedal.publish(Float64(x))
	rospy.sleep(0.1)
	x = x + 0.2

rospy.sleep(1.0)

x = 0.0
for i in range(11):	
	hand_wheel.publish(Float64(x))
	rospy.sleep(0.1)
	x = x - 0.5

rospy.sleep(3.0)

x = 1.0
for i in range(11):	
	gas_pedal.publish(Float64(x))
	rospy.sleep(0.1)
	x = x - 0.1

rospy.sleep(3.0)

x = 0.0
for i in range(11):	
	brake_pedal.publish(Float64(x))
	rospy.sleep(0.1)
	x = x + 0.1
