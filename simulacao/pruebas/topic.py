#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
# pub = rospy.Publisher('topic_name', String)
# rospy.init_node('node_name')
# r = rospy.Rate(10) # 10hz
# while not rospy.is_shutdown():
#    pub.publish("maria fernanda")
#    r.sleep()


# pub = rospy.Publisher('mi_carrito/gas_pedal/cmd', Float64)
# rospy.init_node('gas_pedal')
pub = rospy.Publisher('mi_carrito/brake_pedal/cmd', Float64)
rospy.init_node('brake_pedal')
while not rospy.is_shutdown():
	# str = "hello world %s" % rospy.get_time()
	# rospy.loginfo(str)
	pub.publish(Float64(1.0))
	rospy.sleep(1.0)