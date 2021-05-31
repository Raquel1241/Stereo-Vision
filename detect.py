"""
Document to do facial detection within images.

https://realpython.com/face-recognition-with-python/

at ../xxxxx.jpeg the input images are found.
at ../cascade.xml & ../cascadeEye.xml the face and eye cascades are found

"""

import numpy as np
import cv2
import dist2depth as d2d

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


#### RUN FILE ####
if 0:
	imgPath = "..\img1.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	faces,eyes,ep = detectFace(img)

if 0:
	print("Face locations:")
	print(faces)
	print("\n Eyes locations within face box:")
	print(eyes)
	print('\n')
	i = 0
	while i < len(ep)/2:
		ipd = np.sqrt((ep[2*i][0]-ep[2*i+1][0])**2 + (ep[2*i][1]-ep[2*i+1][1])**2)
		print("Distance between eye centers is: {}".format(ipd))
		i += 1
	#for x,y in ep:
	#	print("{} , {}".format(x,y))

## Atempted disparity calculation
if 1:
	iR = cv2.imread("..\dataset\IMGS\\rightImage_HP000_001_H000_V000.png")
	iR = cv2.cvtColor(iR, cv2.COLOR_BGR2GRAY)
	cv2.imshow("right image",iR)
	iR2 = cv2.equalizeHist(iR)
	iL = cv2.imread("..\dataset\IMGS\leftImage_HP000_001_H000_V000.png")
	iL = cv2.cvtColor(iL, cv2.COLOR_BGR2GRAY)
	cv2.imshow("left image",iL)
	iL2 = cv2.equalizeHist(iL)
	dis1 = d2d.disp(iL,iR)

if 0:
	from matplotlib import pyplot as plt
	yv = []

	imgPath = "..\img_d_50.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 50 cm:")
	faces,eyes,ep = detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	imgPath = "..\img_d_70.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 70 cm:")
	faces,eyes,ep = detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	imgPath = "..\img_d_100.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 100 cm:")
	faces,eyes,ep = detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	imgPath = "..\img_d_140.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 140 cm:")
	faces,eyes,ep = detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	plt.plot([50, 70, 100, 140], yv)
	plt.axis([0,140,0,max(yv)])
	plt.show()