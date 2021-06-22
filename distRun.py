## #!/usr/bin/env python
"""
Python code to run in order to obtain a distance measurement from a video feed.
If Setup has not been performed distSetup.py will be ran first.
"""
# Import section
	# Import libraries
import os
import datetime
import cv2
	# Import own code
import filter as fil
import detect as det
import distSetup
import findDistance as fd
	# Load and/or import variables
from servConf import *

# Global variables setting
setupF 	= "calFile.py" # if changed, also change the import lower
dFile 	= "dist_val.txt"
camOption = None

# Check if setup data is present
#	If present			Ask if resetup needs to be performed
if os.path.isfile(setupF): # Setup file present
	print("Setup file found.")
	newSet = input("Is a new setup required? [Y/N]")
	if newSet[0] == "Y" or newSet[0] == "y":
		distSetup.log(setupF,"calFileOld.py")
		os.remove(setupF)
		print("Old setup file removed after copying to: calFileOld.py")
		distSetup.fullSetup(setupF)
	else:
		print("Continuing with current setup data.")
#	If not present		Notification and run distSetup.py
else: # Setup needed
	print("Setup file not found, setup will be performed.")
	distSetup.fullSetup(setupF)

import calFile as cal # change with setupF variable

# Camera choice
if cal.camOption == 0:
	vid = cv2.VideoCapture(0)
elif cal.camOption == 1:
	if cal.camURL == None:
		camURL = input("Please provide the video steam URL. (eg. protocol://host:port/script_name?script_params|auth)")
	else:
		camURL = cal.camURL
	vid = cv2.VideoCapture(camURL)
else:
	ipCamBool = input("Do you want to use an IP-camera instead of the main video input? [Y/N]")
	if ipCamBool[0] == "Y" or ipCamBool[0] == "y":
		camOption = 1
		camURL = input("Please provide the video steam URL. (eg. protocol://host:port/script_name?script_params|auth)")
		vid = cv2.VideoCapture(camURL)
	else:
		camOption = 0
		vid = cv2.VideoCapture(0)

# Main body
print("Press CTRL+C to exit the loop of capturing, measuring, and sending to the server.")
filVal 	= []	# Filtered diagonal list
invDiag = []		# inverse of diagonal list
calcVal = []		# actual distance
nFal 	= 0			# Amount of no face measurements
while(True):
	try:
		_,frame = vid.read()										# Read video frame
		if cal.camCal == 1:											# provision for undistortion in the future
			a = [] #!!! undistort stuff
		faces,_,_,_ = det.detectEyes(frame)							# Rotate image and extract face bounding boxes
		invDiag = det.fTiD(faces)									# Calculate the inverse diagonals of those bounding boxes
		if not faces:												# No faces detected
			nFal 		+= 1											# Inrement no face detect counter
			invDiag 	= []											# No diagonals, redundant due to det.fTiD output
			if nFal > 15:											# too many no face detects
				filVal 		= []										# reset moving average
		else:														# Faces detected
			nFal 		= 0												# Reset no face counter
			filVal = filVal[:len(invDiag)-1]							# Truncate moving average at the amount of detected faces
		for i in range(len(invDiag)): 								# For every bounding box, apply filtering
			if i >= len(filVal): 										# if not existing, behave as first measurement
				filVal[i] = fil.eWMA(invDiag[i], MA = invDiag[i])			# Begin moving average for i-th face
			else:
				filVal[i] = fil.eWMA(invDiag[i], MA = filVal[i])			# add/update moving average
		for i in range(len(filVal)):								# Loop through EWMA values
			calcVal[i] = fd.diag2distance(filVal[i])					# implement calculation
		f = open(dFile,'a')												# Open file to append measurement
		f.write(calcVal + "\n\t" + datetime.datetime + "\n")			# Add measurement to file
		f.close()														# Close measurement file
		#os.system('scp {} {}@{}:'.format(dFile,serverUser, serverIP))	# Measurement to server
	except KeyboardInterrupt:
		logFile = "dist_val_{}.txt".format(datetime.datetime)			# Make log file name
		distSetup.log(dFile,logFile,1)									# Log measurements when script is stoped
		#os.system('scp {} {}@{}:'.format(logFile, serverUser, serverIP))# Server file log
		vid.release()				# release capture object
		cv2.destroyAllWindows()		# close the video window
		break