#!/bin/bash

fin () {
	killall julius
	exit 1
}

trap fin 1 2 3 15

### remove sticky bit ###
sudo chmod o-t /run/shm/

### run julius ###
( cd ~/dictation-kit/ && julius -C main.jconf -input mic -C am-gmm.jconf -n 1 -module ) &

### run controller ###
./voice_control.py

