#!/usr/bin/env python
# license removed for brevity

import rospy

from std_msgs.msg import Empty
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def move():

    #Defining the publishers for the different topics that this node
    #will publish to.
    landPub = rospy.Publisher('ardrone/land', Empty, queue_size=10)
    takeOffPub = rospy.Publisher('ardrone/takeoff', Empty, queue_size=10)
    resetPub = rospy.Publisher('ardrone/reset', Empty, queue_size=10)
    twistPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    #Initializing the node that the ROS master will look for.
    rospy.init_node('move_node')

    #Defining the twist object that will have access to the six parameter-variables
    #of the Twist class.
    twistObj = Twist()
    emptyObj = Empty()

    rospy.sleep(5)

    #Instructing the drone to takeoff
    rospy.loginfo("AR Drone taking off")
    takeOffPub.publish(emptyObj)
    rospy.sleep(5)

    #Instructing the drone to move forward
    twistObj.linear.x = 0.1
    rospy.loginfo("AR Drone moving forward")
    twistPub.publish(twistObj)
    rospy.sleep(5)

    #Instructing the drone to move backward
    twistObj.linear.x = -0.1
    rospy.loginfo("AR Drone moving backward")
    twistPub.publish(twistObj)
    rospy.sleep(5)

    #Instructing the drone to land
    rospy.loginfo("AR Drone landing")
    landPub.publish(emptyObj)
    rospy.sleep(5)

    rospy.loginfo("Node exiting")


if __name__ == "__main__":
    try:
        move()
    except rospy.ROSInterruptException:
        pass
    
    
    
    
    
    

    
