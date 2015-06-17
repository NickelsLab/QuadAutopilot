/**#include "watershedSegmentation.hpp"


void WatershedSegmenter::setMarkers(const cv::Mat& markerImage) {

// Convert to image of ints
markerImage.convertTo(markers,CV_32S);
}

cv::Mat WatershedSegmenter::process(const cv::Mat &image) {

// Apply watershed
cv::watershed(image,markers);

return markers;
}

// Return result in the form of an image
cv::Mat WatershedSegmenter::getSegmentation() {

cv::Mat tmp;
// all segment with label higher than 255
// will be assigned value 255
markers.convertTo(tmp,CV_8U);

return tmp;
}

// Return watershed in the form of an image
cv::Mat WatershedSegmenter::getWatersheds() {

cv::Mat tmp;
markers.convertTo(tmp,CV_8U,255,255);

return tmp;
}
**/
