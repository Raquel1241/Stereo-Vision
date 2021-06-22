"""
Document to do facial detection within images.

https://realpython.com/face-recognition-with-python/

at ../cascade.xml & ../cascadeEye.xml the face and eye cascades are found

"""

import numpy as np
import cv2
import operator as op
import imutils

dbg = False # Variable to easily turn on or off debug information
font = cv2.FONT_HERSHEY_SIMPLEX

def detectFace(image, debug = dbg):
	"""
	From an input image the face and eye locations are computed. These are returned as 2 variables (faces,eyes).

	IN:		A colour image to extract face and eye locations from
	OUT:	Faces and Eyes locations in the image
	"""
	cascFace = ".\cascade.xml" # Path to the cascade which is the basis of the face detection | haarcascade_frontalface_default | https://github.com/opencv/opencv/tree/master/data/haarcascades
	faceCascade = cv2.CascadeClassifier(cascFace)
	cascEye = ".\cascadeEye.xml"
	eyeCascade = cv2.CascadeClassifier(cascEye)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert colour image to greyscale
	#gray = cv2.equalizeHist(gray) # equalize the histogram of the gray image

	faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
	if debug:print("Found {0} faces!".format(len(faces))) # print how many faces were found

	eyes = []
	ep = []

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		if debug:cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) # Draw rechtangle around face
		### DETECT EYES ###
		faceGray = gray[y:y+h,x:x+w] # Determine ROI to detect eyes within a face box
		eyes = (eyeCascade.detectMultiScale(faceGray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)))
		for (x2,y2,w2,h2) in eyes:
			eyeCenter = (x + x2 + w2//2, y + y2 + h2//2)
			ep.append(eyeCenter)
			if debug:
				radius = int(round((w2 + h2)*0.25))
				cv2.circle(image, eyeCenter, radius, (255, 0, 0 ), 4)

	if debug:
		cv2.imshow("Faces found", image)
		cv2.waitKey(0)
	
	return faces,eyes,ep

def detectEyes(image, debug = dbg):
	"""
	From an image the eyes are detected, in turn the rotation is determined and then the faces after that

	rot, - or + 90 deg, + is to the right side

	IN:		A colour image to extract eye and face locations and rotation
	OUT:	faces,eyes,ep,rot
	"""

	faces = []
	eyes = []
	ep = []
	ang = 0

	cascFace = ".\cascade.xml" # Path to the cascade which is the basis of the face detection | haarcascade_frontalface_default | https://github.com/opencv/opencv/tree/master/data/haarcascades
	faceCascade = cv2.CascadeClassifier(cascFace)
	cascEye = ".\cascadeEye.xml"
	eyeCascade = cv2.CascadeClassifier(cascEye)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert colour image to greyscale
	#gray = cv2.equalizeHist(gray) # equalize the histogram of the gray image

	eyes = eyeCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(20, 20))
	print(eyes)

	a = np.size(eyes,0)

	if a != 2:
		print("Not 1 set eyes detected.")
		faces,_,_ = detectFace(image,debug=debug)
	else:
		x1 = eyes[0][0]+eyes[0][2]/2
		y1 = eyes[0][1]+eyes[0][3]/2
		x2 = eyes[1][0]+eyes[1][2]/2
		y2 = eyes[1][1]+eyes[1][3]/2
		dx = x2 - x1
		dy = y2 - y1
		ang = -45*np.arctan(dy/dx)
		if debug:print("Angle of roatation: {}".format(ang))
		rotatedImg = imutils.rotate_bound(image,ang)
		faces,_,_ = detectFace(rotatedImg,debug=debug)

	
	if debug:
		cv2.imshow("Eyes found", image)
		cv2.waitKey(0)
		i = 0
		for (x, y, w, h) in eyes:
			#cv2.putText(image,"Eye {}".format(i),(x,y),font,1,(255,255,255))
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			i = i + 1
		
	return faces,eyes,ep,ang

def fTiD(faces):
	"""
	Function to transfer faces values to diagonals in a simple list
	"""
	dList = []
	for (x,y,w,h) in faces:
		dList.append(1/np.sqrt(w**2 + h**2))
	return dList
