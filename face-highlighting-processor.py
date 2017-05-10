from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import time
import constants

consumer = KafkaConsumer('video', bootstrap_servers='newton:9092')
producer = KafkaProducer(bootstrap_servers='newton:9092')

cascPath = constants.CLASSIFIER_FILE
faceCascade = cv2.CascadeClassifier(cascPath)

for msg in consumer:
	nparr = np.fromstring(msg.value, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=constants.SCALE_FACTOR,
		minNeighbors=constants.MIN_NEIGHBORS,
		minSize=(constants.MIN_WIDTH, constants.MIN_HEIGHT),
		flags=cv2.CASCADE_SCALE_IMAGE
	)

	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

	img = cv2.imencode('.jpg', img)
	img_str = img[1].tostring()
	producer.send('highlighted-faces', img_str)