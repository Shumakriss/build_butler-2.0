from kafka import KafkaConsumer
import constants

consumer = KafkaConsumer('names', bootstrap_servers=constants.KAFKA_HOST)

for msg in consumer:
	print(msg.value.decode('utf-8'))