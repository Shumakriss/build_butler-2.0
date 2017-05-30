#!/bin/bash

function run {
	python ../kafka_clients/$1 & &> rpi.logs
	echo $! >> .rpi_pids
}

run rpi-audio-producer.py
run rpi-video-producer.py