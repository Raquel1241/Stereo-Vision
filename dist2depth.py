"""
Functions to calculate the depth of objects in stereoscopic images
	Based on stereo vision

	https://www.geeksforgeeks.org/numpy-size-function-python/
Stereo calc:
	https://ijirae.com/volumes/Vol4/iss11/05.NVAE10087.pdf
	https://www.researchgate.net/profile/Manaf-Zivingy/publication/305308988_Object_distance_measurement_by_stereo_vision/links/5788c12d08aeef933e1b9b35/Object-distance-measurement-by-stereo-vision.pdf
OpenCV Stereo doc:
	https://docs.opencv.org/master/dd/d53/tutorial_py_depthmap.html 
"""

from typing import List
import numpy as np
import cv2
from matplotlib import pyplot as plt

bl = None # distance between the 2 camera's
foc = None # Focal distance of the 2 camera's

def dist2depth(dist):
	"""Convert a disparity into a distance/depth"""
	Z = bl*foc/dist
	return Z

def faces2depth(fac1: list, fac2: list):
	"""Convert two lists of face locations in images from stereo cameras to the distance they are away from the cameras

	IN:		two lists of rectangels (x,y,w,h) of all detected faces)
	OUT: 	List of depth
	"""
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

def disp(imL: list, imR: list):
	"""A function to convert 2 grayscale images into a disparity array.
	
	IN:		imageLeft, imageRight (both as greyscale images)
	OUT:	disparityMap
	"""
	stereo = cv2.StereoBM_create()
	stereo.setMinDisparity(1)
	stereo.setNumDisparities(128) # multiple of 16
	stereo.setBlockSize(13)
	stereo.setSpeckleRange(10)
	stereo.setSpeckleWindowSize(8)
	disparity = stereo.compute(imL,imR)
	if 1:
		plt.imshow(disparity,'gray')
		plt.show()
	return disparity

def filter(dList: list, nDist: list):
	"""
	Filter out the outliers, if the new distance measurement has a too large change from the existing list.
	flag is true if the new value is disregarded

	IN:		dList, nDist
	OUT:	nList, flag
	"""
	flag = None
	nList = dList
	if np.absolute(nDist-np.average(dList)) < 750:
		nList.append(nDist)
		flag = False
	else:
		flag = True
	return nList, flag