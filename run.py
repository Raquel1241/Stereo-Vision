"""
Document to run commands with python

at ../xxxxx.jpeg the input images are found.

"""

import numpy as np
import cv2
import dist2depth as d2d
import detect as det
import filter as fil
import time

#### RUN FILE ####
font = cv2.FONT_HERSHEY_SIMPLEX

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
if 0:
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

## Video capture and face detection (averaging filter)
if 1:
	vid = cv2.VideoCapture(0)
	print("Press \'q\' in order to quit capturing video.")


	meas = []
	measT = []
	En = 0
	while(True):	# loop to display video
		ret, frame = vid.read()						# Capture frame by frame
		faces,_,_ = det.detectFace(frame,False) 	# Detect faces in the video
		diag = None

		for (x,y,w,h) in faces: #
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			diag = np.sqrt(2*(faces[0][2]**2))
			cv2.putText(frame,str(1/diag)[0:7],(x,y),font,1,(255,255,255))

		if diag == None:
			En = En + 1
			if En > 5:
				meas = []
				measT = []
			elif len(meas) != 0:
				meas.pop(0)
				measT.pop(0)
			print("No faces were found for {} cycles.".format(En))
			cv2.putText(frame,"No faces were found for {} cycles.".format(En),(0,25),font,1,(255,255,255))
		else:
			En = 0
			meas.append(1/diag)
			measT.append(time.process_time())
			if len(meas) > 0:
				mLpf = fil.avg(meas)
				print("Filtered: \t{}".format(mLpf))
				cv2.putText(frame,"Filtered val: {}".format(mLpf),(0,25),font,1,(255,255,255))
				#meas.pop(0)
				#measT.pop(0)
			print("\t Inverse of diagonal: \t\t {}".format(1/diag))
		
		if len(measT) != 0:
			if (time.process_time() - measT[0] > 5.0):
				print("Pop due to age!! {}".format(time.process_time() - measT[0]))
				meas.pop(0)
				measT.pop(0)

		# Show image with face detected
		cv2.imshow('frame', frame)					# Show the frame
		if cv2.waitKey(1) & 0xFF == ord('q'): break # stop capturing if q is pressed

	vid.release() 				# release capture object
	cv2.destroyAllWindows()		# close the video window

## Video capture and face detection (EWMA)
if 1:
	vid = cv2.VideoCapture(0)
	print("Press \'q\' in order to quit capturing video.")


	meas = []
	movA = None
	En = 0
	while(True):	# loop to display video
		ret, frame = vid.read()						# Capture frame by frame
		faces,_,_ = det.detectFace(frame,False) 	# Detect faces in the video
		diag = None

		for (x,y,w,h) in faces: #
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			diag = np.sqrt(2*(faces[0][2]**2))
			cv2.putText(frame,str(1/diag)[0:7],(x,y),font,1,(255,255,255))

		if diag == None:
			En = En + 1
			if En > 5:
				meas = []
				movA = None
			print("No faces were found for {} cycles.".format(En))
			cv2.putText(frame,"No faces were found for {} cycles.".format(En),(0,25),font,1,(255,255,255))
		else:
			En = 0
			meas.append(1/diag)
			measT.append(time.process_time())
			if (len(meas) > 0) & (movA != None):
				movA = fil.eWMA(meas[-1],movA,lamb = 0.4)
				print("Filtered: \t{}".format(movA))
				cv2.putText(frame,"Filtered val: {}".format(movA),(0,25),font,1,(255,255,255))
			elif (len(meas) > 0) & (movA == None):
				movA = fil.eWMA(meas[-1],meas[-1])
				print("Filtered: \t{}".format(movA))
				cv2.putText(frame,"Filtered val: {}".format(movA),(0,25),font,1,(255,255,255))

			print("\t Inverse of diagonal: \t\t {}".format(1/diag))

		# Show image with face detected
		cv2.imshow('frame', frame)					# Show the frame
		if cv2.waitKey(1) & 0xFF == ord('q'): break # stop capturing if q is pressed

	vid.release() 				# release capture object
	cv2.destroyAllWindows()		# close the video window

## Eye based rotation
if 0:
	picP = "..\img11_1.jpg"
	pic = cv2.imread(picP)
	faces,eyes,ep,r = det.detectEyes(pic)
	print(eyes)
