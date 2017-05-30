from kafka import KafkaConsumer
from kafka import KafkaProducer
import speech_recognition as sr
import constants

r = sr.Recognizer()
consumer = KafkaConsumer('audio', bootstrap_servers=constants.KAFKA_HOST)
producer = KafkaProducer(bootstrap_servers=constants.KAFKA_HOST)

for msg in consumer:
	try:
		audio = sr.AudioData(msg.value, 16000, 2)
		text = r.recognize_google(audio)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
		text = ""
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
		text = ""
	if(text != None or type(text) != type(None)):
		print(text)
		producer.send('text', bytes(text, 'utf-8'))