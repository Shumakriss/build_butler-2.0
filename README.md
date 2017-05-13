# Build Butler 2.0
Version 2.0 of the Build Butler is coming and it's going to be way more flexible. In version 2.0, I aim to simplify BB agents by allowing them to simply publish to Kafka. From there, we can build a master app (or apps) to let us access raw or processed data however we like. This will also pave the way to better integration with tools like SparkStreaming and other ML-related tools for even more advanced IoT-like processing.

## Setup
1. To get started, we use a basic, single-node Kafka setup using the [Quickstart](https://kafka.apache.org/quickstart)
2. Since our consumers/producers are all on different hosts and we want a convenient way to access the broker, we override the listeners and advertised.listeners properties in config/server.properties (an example is checked into the repo).
3. Also, a Dockerized Jenkins is used to kick off the search

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