from kafka import KafkaConsumer
import constants

consumer = KafkaConsumer('text', bootstrap_servers=constants.KAFKA_HOST)

for msg in consumer:
	print(msg.value.decode('utf-8'))