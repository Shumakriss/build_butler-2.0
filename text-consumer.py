from kafka import KafkaConsumer

consumer = KafkaConsumer('text', bootstrap_servers='newton:9092')

for msg in consumer:
	print(msg.value.decode('utf-8'))