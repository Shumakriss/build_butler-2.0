#!/bin/bash

function run {
	python ../$1 &> debug.logs
	echo $! >> .debug_pids
}

run formatted-face-consumer.py
run highlighted-face-consumer.py
run name-consumer.py
run text-consumer.py
run video-consumer.py