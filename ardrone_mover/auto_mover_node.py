#!/usr/bin/env python
# license removed for brevity

import rospy

from std_msgs.msg import Empty
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from tum_ardrone.msg import filter_state

#Initializing the node that the ROS master will look for.
rospy.init_node('move_node', anonymous=True)

#Defining the publishers for the different topics that this node
#will publish to.
landPub = rospy.Publisher('ardrone/land', Empty, queue_size=10)
takeOffPub = rospy.Publisher('ardrone/takeoff', Empty, queue_size=10)
resetPub = rospy.Publisher('ardrone/reset', Empty, queue_size=10)
twistPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

#Defining the twist object that will have access to the six parameter-variables
#of the Twist class. The filter_state object class is for the subscriber and will
#access the variable values from the 
twistObj = Twist()
emptyObj = Empty()
filter_stateObj = filter_state()

#The variable that will represent the state of the drone in the x-direction:
xState = 0.0

def poseCallBack(data):
    xState = data.x
    rospy.loginfo(xState)

def poseListener():
    rospy.Subscriber("ardrone/predictedPose", filter_state, poseCallBack)
    print(xState)
    rospy.spin()

def move():

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

    #Instructing the drone to land
    rospy.loginfo("AR Drone landing")
    landPub.publish(emptyObj)
    rospy.sleep(5)

    rospy.loginfo("Node exiting")


if __name__ == "__main__":
    try:
        poseListener()
        move()
    except rospy.ROSInterruptException:
        pass
    
    
    
    
    
    

    
