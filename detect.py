# https://realpython.com/face-recognition-with-python/
import cv2

def detectFace(image):
	casc = NULL # Path to the cascade which is the basis of the face detection
	faceCascade = cv2.CascadeClassifier(casc)

	# image = cv2.imread(imgPath) # in case the parsed image is not read yet
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE	# Face detection template to use
	)

	print("Found {0} faces!".format(len(faces))) # print how many faces were found
	
	return faces