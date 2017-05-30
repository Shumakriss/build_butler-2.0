# DO NOT RUN: This is just a reference!
FLASK_APP=jenkins-producer.py
flask run --host=0.0.0.0
python laptop-video-producer.py
python face-formatting-processor.py
python face-recognizing-processor.py
python laptop-audio-producer.py
python speech-recognition-processor.py
python search-processor.py