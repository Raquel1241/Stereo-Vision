import cv2
import numpy as np
import time
import detect as det
import filter as fil

debug = True
def distance2invDiag(distance, mlen):
	"""
	Function to determine the inverse diagonal of boudning box using mlen measurements

	INPUT
	distance: distance at which person is sitting
	mlen: how many frames are used for the final measurement

	OUTPUT: inverse of diagonal (averaged over mlen frames)
	"""
	font = cv2.FONT_HERSHEY_SIMPLEX # font on video text

	invDiag = [] # inverse of the diagonal
	avgInvDiag = [] # average of inverse of diagonal over mlen frames

	vid = cv2.VideoCapture(0)
	print("Please sit at a distance of \t{} cm away from the camera".format(distance))
	time.sleep(10) # wait 10 s for the subject to get into place

	while(True):	# loop to display video
		ret, frame = vid.read()						# Capture frame by frame
		faces,_,_ = det.detectFace(frame,False) 	# Detect faces in the video
		diag = None
		
		for (x,y,w,h) in faces: # draw bounding box
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			diag = np.sqrt(2*(faces[0][2]**2))
			cv2.putText(frame,str(1/diag)[0:7],(x,y),font,1,(255,255,255))

		if diag == None: # if no face is detected
			print("No faces were found.")
			cv2.putText(frame,"No face found",(0,25),font,1,(255,255,255))
		else:
			invDiag.append(1/diag) # calculate inverse of diagonal
			if len(invDiag) > mlen: # take mlen measurements
				avgInvDiag = fil.avg(invDiag) # averge measurement
				print("Average inverse diagonal: \t{}".format(avgInvDiag))
				# print on video stream
				cv2.putText(frame,"Average inverse diagonal: {}".format(avgInvDiag),(0,25),font,1,(255,255,255))
				break
			#print("\t Inverse of diagonal: \t\t {}".format(1/diag))
			print(1/diag) # measurement value
		cv2.imshow('frame', frame)					# Show the frame
		if cv2.waitKey(1) & 0xFF == ord('q'): break # stop capturing if q is pressed

	vid.release() 				# release capture object
	cv2.destroyAllWindows()		# close the video window

	return avgInvDiag
	
####### setup function ###############
def setup(distances,mlen):
	"""
	Function to create the function to find distance

	INPUT
	distances: 	distances at which to perform the setup. Array of any size
	mlen:		amount of measurements per calculation of inverse diagonal

	OUTPUT
	a,b: slope and intercept of linear fit 
	"""
	invDiag = [] # list of inverse diagonals corresponding to the distances
	for i in distances: # calculate  inverse diagonal for each distance
		invDiag.append(distance2invDiag(i, mlen))

	a, b = np.polyfit(invDiag, distances, 1)
	return a,b

######## Diagonal 2 distance ##############
def diag2distance(diag):
	"""
	Function to find distance corresponding to diagonal 
	INPUT
	diag: 	diagonal of bounding box
	a:		slope of line
	b:		intercept of line
	"""
	# values are from linear fit, might change to function input
	a = 11352.921196990614 # slope
	b = -2.580169513293289 # intercept
	dist = a*(1/diag)+b
	return dist

def demorun():
	"""
	Show distances on screen
	a, b are the function parameters for diag2distance
	"""
	font = cv2.FONT_HERSHEY_SIMPLEX # font on video text

	vid = cv2.VideoCapture(0)
	while(True):	
		try: # loop to display video
			ret, frame = vid.read()						# Capture frame by frame
			faces,_,_ = det.detectFace(frame,False) 	# Detect faces in the video
			dist = None
			diag = None
			for (x,y,w,h) in faces: # draw bounding box
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				diag = np.sqrt(2*(faces[0][2]**2))
				cv2.putText(frame,str(1/diag)[0:7],(x,y),font,1,(255,255,255))

			if diag == None: # if no face is detected
				print("No faces were found.")
				cv2.putText(frame,"No face found",(0,25),font,1,(255,255,255))
			else:
				dist = diag2distance(diag) # calculate distance
				cv2.putText(frame,"Distance: {}".format(dist),(0,25),font,1,(255,255,255))
				print(dist) # print distance
			cv2.imshow('frame', frame)					# Show the frame
		except KeyboardInterrupt: # stop demo
			vid.release()				# release capture object
			cv2.destroyAllWindows()		# close the video window
			break
		
	return dist

if debug:
	#distances = [50, 70, 100, 150, 170, 200, 250]
	#distances = [30, 35, 40, 45, 50, 60]
	#mlen = 30 # measurement length
	#a,b = setup(distances,mlen)
	#print(a)
	#print(b)
	a = 11352.921196990614 # slope
	b = -2.580169513293289 # intercept
	demorun()