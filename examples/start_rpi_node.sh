#!/bin/bash

function run {
	python ../$1 & &> rpi.logs
	echo $! >> .rpi_pids
}

run rpi-audio-producer.py
run rpi-video-producer.py