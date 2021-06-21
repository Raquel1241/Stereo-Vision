"""
Program to perform a setup procedure.
Needs to be ran in order to perform proper distance measurements.
"""
import os

setupFdefault = "calFile.py"
describtion = '"""\nThis file contains the setup script values. Formatted as python variables, simply import and use.\n"""\n'

def fullSetup(setupF = setupFdefault):
	tmp = describtion
	# Check Input
	camOption = input("""What camera option is prefered?\n\tFor default system camera:\t 0\n\tFor an IP based camera:\t\t 1""")
	if camOption[0] == "0":
		camOption = 0
		camURL = None
	elif camOption[0] == "1":
		camOption = 1
		camURL = input("Please provide the video steam URL. (eg. protocol://host:port/script_name?script_params|auth)")
	else:
		camOption = None
		camURL = None
		print("Please enter a valid camera option.")
	# Calibrate Camera
	cal = input("Does the distortion need to be corrected? [Y/N]")
	if cal[0] == "Y" or cal[0] == "y":
		camCal = 0
		print("Fixing distortion not working yet, continuing without.")
	else:
		camCal = 0
	# Perform validation measurement
	#!!! implement measurement posibly
	# Write calibration data to file
	tmp = tmp + "camOption = " + str(camOption) + "\n"
	tmp = tmp + "camURL = " + str(camURL) + "\n"
	tmp = tmp + "camCal = " + str(camCal) + "\n"
	f = open(setupF,'w')
	f.write(tmp)
	f.close()

def log(fnA, fnB,type = 0):
	"""Append content of fnA to fnB. For overwriting type = 1."""
	f = open(fnA,'r')
	tmp = f.read()
	f.close()
	if type == 1:
		f = open(fnB,'w')
	else:
		f = open(fnB,'a')
	f.write(tmp)
	f.close()