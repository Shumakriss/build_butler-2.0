from kafka import TopicPartition
from kafka import KafkaConsumer
import cv2
import numpy as np
import time
import constants

consumer = KafkaConsumer('video', bootstrap_servers=constants.KAFKA_HOST)

for msg in consumer:
	nparr = np.fromstring(msg.value, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	cv2.imshow("jpg", img)
	k = cv2.waitKey(1)
	if k == ord('q'):
		cv2.destroyAllWindows()