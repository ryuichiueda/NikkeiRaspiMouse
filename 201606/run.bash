#!/bin/bash

( cd ~/dictation-kit/ && julius -C main.jconf -input mic -C am-gmm.jconf -module ) &

./julius/voice_to_robot.py
