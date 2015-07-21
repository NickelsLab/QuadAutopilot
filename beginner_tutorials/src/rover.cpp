#include <cmath>
#include <ctime>
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Empty.h"
#include "geometry_msgs/Twist.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "rover");

  ros::NodeHandle n;
  geometry_msgs::Twist xFieldAccess;
  std_msgs::Empty takeoffAndLand;
  std_msgs::String msg;

  ros::Publisher mover_pub = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
  ros::Publisher takeOff_pub = n.advertise<std_msgs::Empty>("ardrone/takeoff", 1000);
  ros::Publisher land_pub = n.advertise<std_msgs::Empty>("ardrone/land", 1000);
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
  
  ros::Rate loop_rate(.2);
  
  loop_rate.sleep();
  takeOff_pub.publish(takeoffAndLand);
  ROS_INFO("Drone Taking Off");
  //loop_rate.sleep();
 // move_sleepRate.sleep();

  int count = 1;
  
  //clock_t t;
  //t = clock();
  while (ros::ok())
  {

    xFieldAccess.linear.x = 0.07;

    std::stringstream ss;
    ss << "Moving Forward" << count;
    msg.data = ss.str();

    ROS_INFO("%s", msg.data.c_str());

    chatter_pub.publish(msg);
    mover_pub.publish(xFieldAccess);

    ros::spinOnce();
    //  ros::spin();

    //move_sleepRate.sleep();
    ++count;
  }
 //loop_rate.sleep(); 
 //land_pub.publish(takeoffAndLand);
 //ROS_INFO("Drone Landing");

  //t = clock();
  //ROS_INFO("Time Ellapse: [%d]", t);
  return 0;
}
