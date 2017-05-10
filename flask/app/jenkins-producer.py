from flask import Flask, request
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='newton:9092')
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_jenkins_notification():
  build_info = request.get_json()
  json_str = json.dumps(request.get_json())
  print("Received completion notification" + json_str)
  if(build_info['status'] == 'FAILURE'):
    producer.send('jenkins-notifications', json_str.encode('utf-8'))
    print("Posted message")
  return "Notification received"