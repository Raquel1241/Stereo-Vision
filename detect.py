# https://realpython.com/face-recognition-with-python/
import cv2

def detectFace(image):
	casc = "..\haarcascade_frontalface_default.xml" # Path to the cascade which is the basis of the face detection | https://github.com/opencv/opencv/tree/master/data/haarcascades
	faceCascade = cv2.CascadeClassifier(casc)

	#image = cv2.imread(imgPath) # in case the parsed image is not read yet
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.5,
		minNeighbors=5,
		minSize=(40, 40)
		#flags = cv2.CV_HAAR_SCALE_IMAGE	# Face detection template to use
	)

	print("Found {0} faces!".format(len(faces))) # print how many faces were found

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.imshow("Faces found", image)
	cv2.waitKey(0)
	
	return faces


imgPath = "..\img1.jpeg"
img = cv2.imread(imgPath)
faces = detectFace(img)
print(faces)