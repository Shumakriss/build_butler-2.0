import cv2
from kafka import KafkaProducer
import time

video_capture = cv2.VideoCapture(0)
producer = KafkaProducer(bootstrap_servers='newton:9092')

while True:
	time.sleep(0.05)
	ret, frame = video_capture.read()
	img = cv2.imencode('.jpg', frame)
	img_str = img[1].tostring()
	producer.send('video', img_str)