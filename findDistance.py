import cv2
import numpy as np
import time
import detect as det
import filter as fil

font = cv2.FONT_HERSHEY_SIMPLEX

def distance2diag(distance, mlen):
	"""
	INPUT
	distance: distance at which person is sitting
	mlen: how many frames are used for the final measurement

	OUTPUT: inverse of diagonal (averaged of mlen frames)
	"""
	invDiag = [] # inverse of the diagonal
	avgInvDiag = [] # average of inverse of diagonal over mlen frames

	vid = cv2.VideoCapture(0)
	print("Please sit at a distance of \t{} cm away from the camera".format(distance))
	time.sleep(10) # wait 5 s for the subject to get into place

	while(True):	# loop to display video
		ret, frame = vid.read()						# Capture frame by frame
		faces,_,_ = det.detectFace(frame,False) 	# Detect faces in the video
		diag = None
		
		for (x,y,w,h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			diag = np.sqrt(2*(faces[0][2]**2))
			cv2.putText(frame,str(1/diag)[0:7],(x,y),font,1,(255,255,255))

		if diag == None:
			print("No faces were found.")
			cv2.putText(frame,"No face found",(0,25),font,1,(255,255,255))
		else:
			invDiag.append(1/diag)
			if len(invDiag) > mlen:
				avgInvDiag = fil.avg(invDiag) # averge measurement per 10 frames
				print("Average inverse diagonal: \t{}".format(avgInvDiag))
				# print on video stream
				cv2.putText(frame,"Average inverse diagonal: {}".format(avgInvDiag),(0,25),font,1,(255,255,255))
				break
			#print("\t Inverse of diagonal: \t\t {}".format(1/diag))
			print(1/diag)
		cv2.imshow('frame', frame)					# Show the frame
		if cv2.waitKey(1) & 0xFF == ord('q'): break # stop capturing if q is pressed

	vid.release() 				# release capture object
	cv2.destroyAllWindows()		# close the video window
	return avgInvDiag
	
distances = [50, 70, 100, 150, 170, 200, 250]
mlen = 100 # measurement length
diagonals = [] # list of diagonals corresponding to the distances
for i in distances:
	diagonals.append(distance2diag(i, mlen))
