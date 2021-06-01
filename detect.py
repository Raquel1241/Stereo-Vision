"""
Document to do facial detection within images.

https://realpython.com/face-recognition-with-python/

at ../cascade.xml & ../cascadeEye.xml the face and eye cascades are found

"""

import numpy as np
import cv2


debug = True # Variable to easily turn on or off debug information

def detectFace(image):
	"""
	From an input image the face and eye locations are computed. These are returned as 2 variables (faces,eyes).

	IN:		A colour image to extract face and eye locations from
	OUT:	Faces and Eyes locations in the image
	"""
	cascFace = "..\cascade.xml" # Path to the cascade which is the basis of the face detection | haarcascade_frontalface_default | https://github.com/opencv/opencv/tree/master/data/haarcascades
	faceCascade = cv2.CascadeClassifier(cascFace)
	cascEye = "..\cascadeEye.xml"
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
		eyes = eyeCascade.detectMultiScale(faceGray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
		if debug:
			for (x2,y2,w2,h2) in eyes:
				eyeCenter = (x + x2 + w2//2, y + y2 + h2//2)
				ep.append(eyeCenter)
				radius = int(round((w2 + h2)*0.25))
				cv2.circle(image, eyeCenter, radius, (255, 0, 0 ), 4)

	if debug:
		cv2.imshow("Faces found", image)
		cv2.waitKey(0)
	
	return faces,eyes,ep
