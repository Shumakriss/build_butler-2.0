#!/bin/bash

function run {
	python ../$1 & &> processor.logs
	echo $! >> .processor_pids
}

run face-formatting-processor.py
run face-highlighting-processor.py
run face-recognizing-processor.py
run speech-recognition-processor.py