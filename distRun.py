"""
Python code to run in order to obtain a distance measurement from a video feed.
If Setup has not been performed distSetup.py will be ran first.
"""
# Import section
import os
import distSetup

import filter as fil
import detect as det
import cv2

# Global variables setting
setupF = "calFile.txt"
camOption = None

# Check if setup data is present
#	If present			Ask if resetup needs to be performed
if os.path.isfile(setupF): 								# Setup file present
	print("Setup file found.")
	f = open(setupF,'r')
	newSet = input("Is a new setup required? [Y/N]")
	if newSet[0] == "Y":
		distSetup.fullSetup(setupF)
	else:
		print("Continuing with current setup data.")
#	If not present		Notification and run distSetup.py
else:													# Setup needed
	print("Setup file not found, setup will be performed.")
	distSetup.fullSetup(setupF)

# Main body
if camOption == 0:
	vid = cv2.VideoCapture(0)
elif camOption == 1:
	camIP = input("Please provide the video steam URL. (eg. protocol://host:port/script_name?script_params|auth)")
	vid = cv2.VideoCapture(camIP)
else:
	ipCamBool = input("Do you want to use an IP-camera instead of the main video input? [Y/N]")
	if ipCamBool == "Y":
		camOption = 1
		camIP = input("Please provide the video steam URL. (eg. protocol://host:port/script_name?script_params|auth)")
		vid = cv2.VideoCapture(camIP)
	else:
		camOption = 0
		vid = cv2.VideoCapture(0)

print("Press CTRL+C to exit the loop of capturing, measuring, and sending to the server.")
while(True):
	try:
		a = 1	# placeholder
		#measure
		#	Rotation if 2 eyes
		#	Detection -> BB
		#filter
		#	eWMA of diag
		#calculate
		#send to server
	except KeyboardInterrupt:
		# Release all capture elements and stuff
		vid.release()				# release capture object
		cv2.destroyAllWindows()		# close the video window
		break