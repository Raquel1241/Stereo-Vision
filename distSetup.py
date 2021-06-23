"""
Program to perform a setup procedure.
Needs to be ran in order to perform proper distance measurements.
"""
import os
import findDistance as fd

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
		print("Fixing distortion is not working yet, continuing without.")
	else:
		camCal = 0
	# Perform validation measurement
	tmp0 = input("At what distances will the setup be performed? (in centimeters)\n\tPlease sepperate them by comma's without spaces in between. (example: '30,50,100,170,250')")
	tmp0 = list(map(int,tmp0.split(',')))
	tmp1 = input("How many setup measurements will be taken per distance? [20-40], 30 is recomended")
	tmp1 = int(tmp1)
	if camOption == 0:
		setA,setB = fd.setup(tmp0,tmp1)
	else:
		setA,setB = fd.setup(tmp0,tmp1,camURL=camURL)
	print("Please confirm the measurements are accurate the first time the program is ran.")
	# Write calibration data to file
	tmp = tmp + "camOption = " + str(camOption) + "\n"
	tmp = tmp + "camURL = " + str(camURL) + "\n"
	tmp = tmp + "camCal = " + str(camCal) + "\n"
	tmp = tmp + "A = " + str(setA) + "\n"
	tmp = tmp + "B = " + str(setB) + "\n"
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