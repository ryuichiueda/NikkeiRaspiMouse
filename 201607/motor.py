#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Int32MultiArray

def callback_motor_sw(message):
    with open('/dev/rtmotoren0','w') as f:
        if message.data: print >> f, '1'
        else:            print >> f, '0'

    return True

def callback_motor_raw(message):
    try:
        lf = open('/dev/rtmotor_raw_l0','w')
        rf = open('/dev/rtmotor_raw_r0','w')
        print >> lf, str(message.data[0])
        print >> rf, str(message.data[1])
    except:
        print >> sys.stderr, "cannot write to rtmotor_raw_*" 
        sys.exit(1)
    else:
        lf.close()
        rf.close()

if __name__ == '__main__':
    rospy.init_node('rtmotor')
    sub_sw = rospy.Subscriber('switch_motors', Bool, callback_motor_sw)
    sub_raw = rospy.Subscriber('motor_raw', Int32MultiArray, callback_motor_raw)
    rospy.spin()
