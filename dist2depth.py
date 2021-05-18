# Fucntion to calculate the depth of an object from the distance between the centers of object detection based boxes
#
#	https://www.geeksforgeeks.org/numpy-size-function-python/
#
import numpy as np
#import cv2
bl = None # distance between the 2 camera's
foc = None # Focal distance of the 2 camera's

# if distance between faces is computed beforehand
def dist2depth(dist):
	Z = bl*foc/dist
	return Z

# if faces variable is parced
def faces2depth(fac1, fac2):
	if np.size(fac1,0) != np.size(fac2,0):
		print("An error occured with detecting faces")
	else:
		# Calculate the center of the rectangles and asses the distance to them