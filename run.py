"""
Document to run commands with python

at ../xxxxx.jpeg the input images are found.

"""

import numpy as np
import cv2
import dist2depth as d2d
import detect as det

#### RUN FILE ####

## Single face detection run
if 0:
	imgPath = "..\img1.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	faces,eyes,ep = det.detectFace(img)

## Distance between eyes
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

## Diagonal of faces and the inverse
if 0:
	from matplotlib import pyplot as plt
	yv = []

	imgPath = "..\img_d_50.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 50 cm:")
	faces,eyes,ep = det.detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	imgPath = "..\img_d_70.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 70 cm:")
	faces,eyes,ep = det.detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	imgPath = "..\img_d_100.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 100 cm:")
	faces,eyes,ep = det.detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	imgPath = "..\img_d_140.jpeg" # enter file for faces to be detected in
	img = cv2.imread(imgPath)
	print("Face 140 cm:")
	faces,eyes,ep = det.detectFace(img)
	diag = np.sqrt(2*(faces[0][2]**2))
	yv.append(1/diag)
	print(faces)
	print("\t Diagonal: \t {}".format(diag))
	print("\t Inverse of diagonal: \t\t {}".format(1/diag))

	plt.plot([50, 70, 100, 140], yv)
	plt.axis([0,140,0,max(yv)])
	plt.show()
