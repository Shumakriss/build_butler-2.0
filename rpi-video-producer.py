import cv2
import picamera
from kafka import KafkaProducer
import time

video_capture = cv2.VideoCapture(0)
producer = KafkaProducer(bootstrap_servers='newton:9092')

while True:
	time.sleep(0.04)
	ret, frame = video_capture.read()
	img = cv2.imencode('.jpg', frame)
	img_str = img[1].tostring()

	output = None
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.framerate = 24
		output = np.empty((240, 320, 3), dtype=np.uint8)
		camera.capture(output, 'rgb')
	return output

	producer.send('rpi-video', img_str)