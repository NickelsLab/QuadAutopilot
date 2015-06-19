import numpy as np
import sys,cv2

cap = cv2.VideoCapture('../vid1.m4v');
if not cap.isOpened():
	print "Cannot open the video file"
	exit

fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
print "Frames per second :",fps

cv2.namedWindow("MyVideo")
f=1;
while True:
	try:
		# print "f=",f
		f = f+1
		bSuccess,frame = cap.read()
		if not bSuccess:
			print "Can't read the frame from the video file"
			break
		grayframe = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		ret,thresh = cv2.threshold(grayframe,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		kernel = np.ones((5,5),np.uint8)
		fg = cv2.erode(thresh,kernel,iterations=1)

		# noise removal
		opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

		img = opening

		# identify the starting point
		(hei,wid) = img.shape
		center_x = wid/2
		center_y = hei-20

		# go UP till you find foreground
		while (center_y>0 and img[center_y,center_x] != 0):
			center_y = center_y - 1
		if (center_y==0):
			print "couldn't find starting point"
			break
		# go LEFT till you find background
		left_x = center_x
		while (left_x>0 and img[center_y,left_x] == 0):
			left_x = left_x - 1
		# go RIGHT till you find background
		right_x = center_x
		while (right_x<wid and img[center_y,right_x] == 0):
			right_x = right_x + 1

		# here is the final target
		tgt_x = (right_x + left_x) / 2
		
		#cv2.circle(img, (center_x,center_y), 50, (128,128,128),10)
		cv2.circle(img, (left_x,center_y), 50, (128,128,128),10)
		cv2.circle(img, (right_x,center_y), 50, (128,128,128),10)
		cv2.arrowedLine(img,(center_x,center_y),(tgt_x,center_y-100),(128,128,128),10)
		
		cv2.imshow("MyVideo",img)
		cv2.waitKey(1)
	except KeyboardInterrupt:
		print "shutting down"
		cv2.destroyAllWindows()
		for i in range(10):
			cv2.waitKey(1)
		raise

print "shutting down"
cv2.destroyAllWindows()
for i in range(10):
	cv2.waitKey(1)
sys.exit()
