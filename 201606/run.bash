#!/bin/bash

fin () {
	killall julius
	exit 1
}

trap fin 1

( cd ~/dictation-kit/ && julius -C main.jconf -input mic -C am-gmm.jconf -n 1 -module ) &

./voice_control.py

