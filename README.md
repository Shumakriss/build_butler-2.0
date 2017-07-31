# Build Butler 2.0
Version 2.0 of the Build Butler is coming and it's going to be way more flexible. In version 2.0, I aim to simplify BB agents by allowing them to simply publish to Kafka. From there, we can build a master app (or apps) to let us access raw or processed data however we like. This will also pave the way to better integration with tools like SparkStreaming and other ML-related tools for even more advanced IoT-like processing.

## Setup
1. To get started, we use a basic, single-node Kafka setup using the [Quickstart](https://kafka.apache.org/quickstart)
* Or use docker, but first export KAFKA_HOST=$(echo $DOCKER_HOST | sed 's/.*\/\///g' | sed 's/:.*//g')
2. Since our consumers/producers are all on different hosts and we want a convenient way to access the broker, we override the listeners and advertised.listeners properties in config/server.properties (an example is checked into the repo).
3. Also, a Dockerized Jenkins is used to kick off the search
4. Lastly, spin up the various Python processes. You will need either laptop or RPI producers for both video and audio. You will need all of the files ending in "-processor.py" and any consumers you wish for debugging.

## Build Butler in Action

Nothing like that just woke up look!

* Getting the video stream
<img src="https://raw.githubusercontent.com/Shumakriss/build_butler-2.0/master/docs/images/video_consumer.png?raw=true"/>

* Detect faces
<img src="https://github.com/Shumakriss/build_butler-2.0/blob/master/docs/images/face-highlighting.png?raw=true"/>

* Format faces for recognition
<img src="https://github.com/Shumakriss/build_butler-2.0/blob/master/docs/images/face-formatting.png?raw=true"/>

* Put a name to the face
<img src="https://github.com/Shumakriss/build_butler-2.0/blob/master/docs/images/face-naming.png?raw=true"/>

* Get text from audio
<img src="https://github.com/Shumakriss/build_butler-2.0/blob/master/docs/images/speech-recognizing.png?raw=true"/>


## Project Direction
* More infrastructure-as-code with Docker Compose
	* Dockerize Zookeeper, Kafka, and Jenkins
	* Dockerize processor agents, backends, and clients
* Use Streams API for:
	* Merging images into single dashboard stream
	* Determining when all the search criteria are met (face, verbal acknowledgment, etc.)
	* Pathfinding algorithms that require several data streams
* Introduce more hardware
	* iRobot Create
	* Parrot AR Drone
	* Additional RPi sensors (IR, SONAR, Altimeter, GPS, Accelerometer)
	* Seeking recommendations for R2D2, BB-8, and Robot B-9 M-3 platforms as well!
* Make better use of data
	* Allow alert notifications from anomaly detection
	* Use NiFi to pump data to Hadoop, Spark, etc.
	* Send data to cloud for better GPU compute
	* Build better models using the data and SOTA methods
