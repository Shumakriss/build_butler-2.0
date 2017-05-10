from kafka import KafkaProducer
import time
import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

producer = KafkaProducer(bootstrap_servers='newton:9092')

def callback(recognizer, audio):
	print("Volume threshold reached, sending data")
	producer.send('audio', audio.get_raw_data())

stop_listening = r.listen_in_background(m, callback)

while True:
	time.sleep(600)