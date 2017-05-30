#!/bin/bash

function run {
	python ../kafka_clients/$1 & &> processor.logs
	echo $! >> .processor_pids
}

export KAFKA_HOST=$(echo $DOCKER_HOST | sed 's/.*\/\///g' | sed 's/:.*//g')

docker-compose up -d

run face-formatting-processor.py
run face-highlighting-processor.py
run face-recognizing-processor.py
run speech-recognition-processor.py