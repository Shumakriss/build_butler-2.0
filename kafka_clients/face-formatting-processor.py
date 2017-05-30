from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import time
import constants

def crop(x, y, w, h):
    # If it's wider
    if( w/h > constants.RATIO):
        # Expand width
        extra_width = (92 * h / 112) - w
        w = w + extra_width
        x = x - (extra_width / 2)
    # If it's narrower
    else:
        # Expand height
        extra_height = (112 * w / 92) - h
        h = h + extra_height
        y = y - (extra_height / 2)
    return int(x), int(y), int(w), int(h)

consumer = KafkaConsumer('video', bootstrap_servers=constants.KAFKA_HOST)
producer = KafkaProducer(bootstrap_servers=constants.KAFKA_HOST)

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

	for i, (x, y, w, h) in enumerate(faces):
		x, y, w, h = crop(x, y, w, h)
		face = gray[y:y+h, x:x+w]
		resized = cv2.resize(face, (92, 112))
		img = cv2.imencode('.jpg', resized)
		img_str = img[1].tostring()
		producer.send('formatted-faces', img_str)