from kafka import KafkaConsumer
from subprocess import call
import time
import timeout_decorator
import json
from pygame import mixer
import constants

mixer.init()
mixer.music.load('ride_of_the_valkyries.mp3')

jenkins = KafkaConsumer('jenkins-notifications', bootstrap_servers=constants.KAFKA_HOST)
names = KafkaConsumer('names', bootstrap_servers=constants.KAFKA_HOST)
text = KafkaConsumer('text', bootstrap_servers=constants.KAFKA_HOST)

WAIT_JENK = "Waiting for Jenkins notification"
RCV_JENK = "Received Jenkins notification"

def found(person):
	print("Found Chris!")
	call(["say", "-v", "Karen", "Chris, you broke the build."])
	call(["say", "-v", "Karen", "Do you understand?"])

@timeout_decorator.timeout(30)
def wait_for_verbal_ack():
	for text_msg in text:
		text_str = text_msg.value.decode('utf-8')
		print(text_str)
		if( text_str == 'yes'):
			call(["say", "-v", "Karen", "Good, now fix it!"])
			break

@timeout_decorator.timeout(600)
def wait_for_face(username):
	print("Looking for " + username)
	call(["say", "-v", "Karen", "Looking for " + username])
	for name in names:
		names.pause()
		face = name.value.decode('utf-8')
		if( face == username):
			mixer.music.fadeout(2 * 1000)
			found(username)
			try:
				wait_for_verbal_ack()
			except timeout_decorator.timeout_decorator.TimeoutError:
				print("Retry")
			break
		else:
			names.resume()
		names.seek_to_end()

print(WAIT_JENK)
for jenkins_msg in jenkins:
	print(RCV_JENK)
	mixer.music.play(start=4.0)
	build_info_str = jenkins_msg.value.decode('utf-8')
	build_info = json.loads(build_info_str)
	status = build_info['status']
	username = build_info['username'].split(" ")[0].lower()
	wait_for_face(username)
	print(WAIT_JENK)