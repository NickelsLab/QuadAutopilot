#include "ros/ros.h"
#include <iostream>
#include <fstream>
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "ws.h"

using namespace std;
using namespace cv;
double kValue = -1.9;
int a1 = 0; //left Corner
int a2 = 0; //Right Corner

int hallwayCenter;
int imageProcess(Mat frame);

cv_bridge::CvImagePtr cv_ptr;
Mat inputImage;
string name;
stringstream sstm;


void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{  
  try
  {
    int count;
    int centerError;
    double yawValue;
    
    
    count++;
    name = "convertedImage";
    sstm<<name<<count;
    ROS_INFO("Image subscribed");
    
    //cv::imshow("View", cv_bridge::toCvCopy(msg, "mono8")->image);
    

    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);

//ROS_INFO("Part 1");

    inputImage = cv_ptr->image;
//ROS_INFO("Part 2");

    imwrite(sstm.str()+".jpg", inputImage);

//ROS_INFO("Part 3");
    yawValue = imageProcess(inputImage);


    ROS_INFO("Yaw Value: [%f]", yawValue);
    cv::waitKey(1000);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
  }


}

int imageProcess(cv::Mat frame)
{

int countLabel = 0;

//ROS_INFO("Part 4");

    Mat grayFrame;
//ROS_INFO("Part 5");

    cvtColor(frame,grayFrame,CV_RGB2GRAY);
//ROS_INFO("Part 6");

    //Watershed Segmentation


        // Get the binary map
           cv::Mat binary;
           //binary = cv::imread("binary.bmp", 0); // prevent loading of pre-converted image
           cvtColor(frame, grayFrame, CV_BGR2GRAY); // instead convert original
           grayFrame = grayFrame < 60; // apply threshold

           // Display the binary image
           cv::namedWindow("Binary Image");
        //   cv::imshow("Binary Image", grayFrame);

           // Eliminate noise and smaller objects
           cv::Mat fg;
           cv::erode(grayFrame, fg, cv::Mat(), cv::Point(-1, -1), 6);

           // Display the foreground image
        //   cv::namedWindow("Foreground Image");
        //   cv::imshow("Foreground Image", fg);

           // Identify image pixels without objects
           cv::Mat bg;
           cv::dilate(grayFrame, bg, cv::Mat(), cv::Point(-1, -1), 6);
           cv::threshold(bg, bg, 1, 128, cv::THRESH_BINARY_INV);

           // Display the background image
          // cv::namedWindow("Background Image");
         //  cv::imshow("Background Image", bg);

           // Show markers image
           cv::Mat markers(grayFrame.size(), CV_8U, cv::Scalar(0));
           markers = fg + bg;
          // cv::namedWindow("Markers");
         //  cv::imshow("Markers", markers);

          // Create watershed segmentation object
           WatershedSegmenter segmenter;
           // Set markers and process
           segmenter.setMarkers(markers);
           segmenter.process(frame);
//ROS_INFO("Part 7");
   cv::Mat mutableImage;
   mutableImage = segmenter.getSegmentation();
   
   string name = "simpleWall";
   
   std::stringstream sstm;
   sstm << name << hallwayCenter;
   ++countLabel;
   
   imwrite(sstm.str()+".jpg", segmenter.getSegmentation());

   cv::namedWindow("testVision");
   cv::imshow("testVision",mutableImage);
  // cv::imwrite("imgForPoster", mutableImage);

//ROS_INFO("Part 8");

   //Set starting x,y values

           int y_ex= 260;
           int x_ex= 320;


//ROS_INFO("Part 9");

Scalar intensity; 

           for (int i=x_ex; i>0; i--) {
//ROS_INFO("Part 9.1");
        	   Scalar intensity = (int)mutableImage.at<uchar>(y_ex, i);
//ROS_INFO("Part 9.2");
        	   Scalar intensity1 = (int)mutableImage.at<uchar>(y_ex, i-10);
//ROS_INFO("Part 9.3");
        	   int floorVal= (int)*intensity.val;
//ROS_INFO("Part 9.4");
        	   int floorVal1= (int)*intensity1.val;

           if (floorVal==128 && floorVal1!= 128 ){
//ROS_INFO("Part 9.41");
        	           		   a1=i;

           }


           }

//ROS_INFO("Part 10");

           for (int i=x_ex; i<590; i++) {
        	   Scalar intensity = (int)mutableImage.at<uchar>(y_ex, i);
        	   Scalar intensity2 = (int)mutableImage.at<uchar>(y_ex, i+30);
        	   int floorVal= (int)*intensity.val;
        	   int floorVal2= (int)*intensity2.val;

        	   if(floorVal==128 && floorVal2 != 128) {
        		   a2=i;
        	   }
           }

//ROS_INFO("Part 11");

           hallwayCenter=(a1+a2)/2;
           int imageCenter= 300;
//ROS_INFO("Part 12");
           int error= hallwayCenter-imageCenter;

//ROS_INFO("Part 13");

     	   double tempYawValue= error*kValue;

	   double yawArray[10000];
   
           yawArray[countLabel] = tempYawValue;
           
           


           //MAIN Y Value for ROS implemenation. Should be teling me where the center is in relation to one of the walls.
//ROS_INFO("Part 14");

            putText(mutableImage, "X", cvPoint(hallwayCenter,y_ex), 0, 2.5, cvScalar(0,0,0,255), 3, CV_AA);
             cout<<"It is working "<<hallwayCenter;
//ROS_INFO("Part 15");
 

//ROS_INFO("Part 16");
ROS_INFO("Frame Error:  [%d]", error); 
ros::NodeHandle n; 
ros::Publisher tempYawValue_pub = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
geometry_msgs::Twist yaw_access;


yaw_access.angular.z = tempYawValue;


tempYawValue_pub.publish(yaw_access);

for(int i = 0; i < 10000; i++)
{
   ROS_INFO("y[%f] ",yawArray[i]);
}

return tempYawValue;

}

int main(int argc, char **argv)
{

  ros::init(argc, argv, "image_subscriber");
  ros::NodeHandle nh;
  ros::Rate loop_rate(.10);
  //cv::namedWindow("View");
  loop_rate.sleep();
  startWindowThread();
  image_transport::ImageTransport it(nh);
  image_transport::Subscriber sub = it.subscribe("ardrone/front/image_raw", 1, imageCallback);
  //ros::Publisher yawValue_pub = nh.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
  //yawValue_pub.
  
  
  
  ros::spin();
  
  //cv::destroyWindow("View"); 
  return 0;
}
