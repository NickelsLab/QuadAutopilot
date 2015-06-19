import numpy as np
import cv2

print "starting up"
img = cv2.imread('/home/knickels/Documents/Pics/image08.jpg',0)
cv2.imshow('my image',img)
print "waiting on you"
cv2.waitKey(500)


print "shutting down"
cv2.destroyAllWindows()
for i in range(10):
	cv2.waitKey(1)
