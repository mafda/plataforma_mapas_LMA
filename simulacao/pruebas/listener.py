#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64


def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %d" % data.data)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("mi_carrito", Float64, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()