# https://realpython.com/face-recognition-with-python/
import cv2

def detectFace(image):
	cascFace = "..\cascade.xml" # Path to the cascade which is the basis of the face detection | haarcascade_frontalface_default | https://github.com/opencv/opencv/tree/master/data/haarcascades
	faceCascade = cv2.CascadeClassifier(cascFace)
	cascEye = "..\cascadeEye.xml"
	eyeCascade = cv2.CascadeClassifier(cascEye)

	#image = cv2.imread(imgPath) # in case the parsed image is not read yet
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#gray = cv2.equalizeHist(gray) # equalize the histogram of the gray image

	faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(40, 40)) #, flags = cv2.CV_HAAR_SCALE_IMAGE)	# Face detection template to use
	print("Found {0} faces!".format(len(faces))) # print how many faces were found

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		### DETECT EYES ###
		faceGray = gray[y:y+h,x:x+w]
		eyes = eyeCascade.detectMultiScale(faceGray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
		for (x2,y2,w2,h2) in eyes:
			eyeCenter = (x + x2 + w2//2, y + y2 + h2//2)
			radius = int(round((w2 + h2)*0.25))
			cv2.circle(image, eyeCenter, radius, (255, 0, 0 ), 4)


	cv2.imshow("Faces found", image)
	cv2.waitKey(0)
	
	return faces


imgPath = "..\img1.jpeg" # enter file for faces to be detected in
img = cv2.imread(imgPath)
faces = detectFace(img)
print("Face locations:")
print(faces)