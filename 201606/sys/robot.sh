#!/bin/sh -evx
exec 2> /run/shm/init.log

### set the driver ###
insmod /home/ubuntu/RaspberryPiMouse/src/drivers/rtmouse.ko ||
insmod /home/ubuntu/RaspberryPiMouse/lib/Pi?B+/`uname -r`/rtmouse.ko 
sleep 1
chmod 666 /dev/rt*

### motor power off ###
echo 0 > /dev/rtmotoren0
