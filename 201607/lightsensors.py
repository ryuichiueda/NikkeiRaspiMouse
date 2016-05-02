#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Int32MultiArray

rospy.init_node('lightsensors')
pub = rospy.Publisher('lightsensors', Int32MultiArray, queue_size=2)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    with open('/dev/rtlightsensor0','r') as f:
        data = f.readline().split()
        d = Int32MultiArray()
        d.data = [ int(x) for x in data ]
        d.data.reverse()
        pub.publish(d)
        rate.sleep()

