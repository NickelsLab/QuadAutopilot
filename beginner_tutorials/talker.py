#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)

    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    rospy.sleep(5)

    rospy.loginfo("Node exiting")


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
