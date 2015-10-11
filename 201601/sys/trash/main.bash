#!/bin/bash -xv

exec &> /run/shm/main.log
core=$(dirname $0)

while true ; do
	###init###
	echo 0 | tee /dev/rtled?	###LEDを消す###
	echo 0 | tee /dev/rtmotor[_e]*	###モータを止める###

	#準備完了の合図
	echo 1000 > /dev/rtbuzzer0
	sleep 0.2
	echo 0 > /dev/rtbuzzer0
	echo 1 > /dev/rtled0
	$core/wait_sw_push 0
	$core/wait_sw_unpush 0

	###set###
	echo 100 > /dev/rtbuzzer0	###モータ励磁の警告音を出す###
	echo 1 > /dev/rtmotoren0	###モータ励磁###

	#準備完了の合図
	echo 1 > /dev/rtled1
	$core/wait_sw_push 0
	$core/wait_sw_unpush 0

	###run###
	#run.py起動の合図
	echo 0 > /dev/rtbuzzer0
	echo 1 > /dev/rtled2
        $core/../run.py &

	###wait the finish button###
	$core/wait_sw_push 0
	$core/wait_sw_unpush 0
        killall -1 run.py
done
