#!/bin/bash

function run {
	python ../kafka_clients/$1 &> laptop.logs &
	echo $! >> .laptop_pids
}

run laptop-audio-producer.py
run laptop-video-producer.py