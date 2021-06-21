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
	# Load and/or import variables
from servConf import *

# Global variables setting
setupF 	= "calFile.py" # if changed, also change the import lower
dFile 	= "dist_val.txt"
camOption = None

# Check if setup data is present
#	If present			Ask if resetup needs to be performed
if os.path.isfile(setupF): 								# Setup file present
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
else:													# Setup needed
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
while(True):
	try:
		_,frame = vid.read()
		if cal.camCal == 1:
			a = 1 #!!! undistort stuff
		#	measure
		#		Rotation if 2 eyes
		faces,_,_,_ = det.detectEyes(frame)
		#		Detection -> BB
		#.bbDiag = det.fTD(faces)
		#	filter
		#		eWMA of diag
		filVal = None
		#	calculate
		calcVal = None
		#	put measurement in file
		#.f = open(dFile,'a')
		#.f.write(calcVal + "\n")
		#.f.close()
		#	send to server
		#.os.system('scp dist_val.txt {}@{}:'.format(serverUser, serverIP))
	except KeyboardInterrupt:
		# 	Log measurements when script is stoped
		logFile = "dist_val_{}.txt".format(datetime.datetime)
		distSetup.log(dFile,logFile,1)
		# 	Server file log
		os.system('scp {} {}@{}:'.format(logFile, serverUser, serverIP))
		# 	Release all capture elements and stuff
		vid.release()				# release capture object
		cv2.destroyAllWindows()		# close the video window
		break