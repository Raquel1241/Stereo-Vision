"""
Program to perform a setup procedure.
Needs to be ran in order to perform proper distance measurements.
"""
setupFdefault = "calFile.txt"

def fullSetup(setupF = setupFdefault):
	# Check if there's an old calibration file and remove if confirmed

	# Check Input

	# Calibrate Camera

	# Perform validation measurement

	# Write calibration data to file
	calVal = "{},{}".format(None,None)
	f = open(setupF,'w')
	f.write(calVal)
	f.close()