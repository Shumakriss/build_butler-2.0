#!/bin/bash

function run {
	python ../kafka_clients/$1 &> debug.logs
	echo $! >> .debug_pids
}

run video-consumer.py
run highlighted-face-consumer.py
run formatted-face-consumer.py
run name-consumer.py
run text-consumer.py