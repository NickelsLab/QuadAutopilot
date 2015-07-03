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

landPub = rospy.Publisher('ardrone/land', Empty, queue_size = 200)
takeOffPub = rospy.Publisher('ardrone/takeoff', Empty, queue_size = 200)
resetPub = rospy.Publisher('ardrone/reset', Empty, queue_size = 200)
twistPub = rospy.Publisher('cmd_vel', Twist, queue_size = 200)

def callback(data):
    process(data.x)
    rospy.loginfo("Receiving nav data")

def process(xStateVal):
    if xStateVal > 0.2:
        twistObj.linear.x = -0.5
        twistPub.publish(twistObj)
        rospy.loginfo("Successful")
    else:
        landPub.publish(emptyObj)
        rospy.loginfo("Landing")


def subscriberFunction():
    rospy.Subscriber("ardrone/predictedPose", filter_state, callback)
    rospy.spin()

def takeOff():

    #Without this sleep, the drone will not take off most likely because
    #there needs to be enough time for the node to initialize before messages
    #are published to the topics. 
    rospy.sleep(3);

    #Resets the AR Drone at the beginning of this node, i.e. at the instant
    #before take off.
    resetPub.publish(emptyObj)
    rospy.loginfo("Drone reset")
    rospy.sleep(1)
    
    takeOffPub.publish(emptyObj)
    rospy.loginfo("Taking off")
    rospy.sleep(5)

def moveForward():
    rospy.sleep(3)
    twistObj.linear.x = 0.5
    twistPub.publish(twistObj)
    rospy.loginfo("Moving forward")

if __name__ == '__main__':
    try:
        takeOff()
    except rospy.ROSInterruptException:
            pass
    try:
        moveForward()
    except rospy.ROSInterruptException:
            pass
    rospy.sleep(4)
    subscriberFunction()
