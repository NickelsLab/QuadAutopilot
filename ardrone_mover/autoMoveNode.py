#!/usr/bin/env python

import rospy

from tum_ardrone.msg import filter_state
from std_msgs.msg import Empty
from std_msgs.msg import String
from geometry_msgs.msg import Twist

rospy.init_node('autoMoveNode', anonymous=True)

twistObj = Twist()
emptyObj = Empty()
filterStateObj = filter_state()

landPub = rospy.Publisher('ardrone/land', Empty, queue_size = 20)
takeOffPub = rospy.Publisher('ardrone/takeoff', Empty, queue_size = 20)
resetPub = rospy.Publisher('ardrone/reset', Empty, queue_size = 20)
twistPub = rospy.Publisher('cmd_vel', Twist, queue_size = 20)

def callback(data):
    process(data.x)

def process(xStateVal):
    if xStateVal > 0.03:
        twistObj.linear.x = -0.1
        twistPub.publish(twistObj)
    else:
        landPub.publish(emptyObj)


def subscriberFunction():
    rospy.Subscriber("ardrone/predictedPose", filter_state, callback)
    rospy.spin()

def moveForward():
    takeOffPub.publish(emptyObj)
    rospy.sleep(2)

    twistObj.linear.x = 0.1
    twistPub.publish(twistObj)

if __name__ == '__main__':
    try:
        moveForward()
        except rospy.ROSInterruptionException:
            pass
    rospy.sleep(10)
    subscriberFunction()
