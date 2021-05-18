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

# if faces variables are parced (two lists of rectangels (x,y,w,h) of all detected faces)
def faces2depth(fac1, fac2):
	dir = 0 # the direction in which the arrays are filled with faces | https://numpy.org/doc/stable/reference/generated/numpy.ma.size.html
	if np.size(fac1,dir) != np.size(fac2,dir):
		print("An error occured with detecting faces")
	else:
		# Calculate the center of the rectangles and asses the distance to them
		x1 = []
		x2 = []
		d = []
		D = []
		for i in range(np.size(fac1,dir)):
			x1[i] = fac1[i][0]+fac1[i][2]/2
			x2[i] = fac2[i][0]+fac2[i][2]/2
			d[i] = x1[i] - x2[i]
			D[i] = dist2depth(d[i])
		'''	
		for (x,y,w,h) in fac1:
			x1 = x+w/2
		for (x,y,w,h) in fac2:
			x2 = x+w/2
		'''