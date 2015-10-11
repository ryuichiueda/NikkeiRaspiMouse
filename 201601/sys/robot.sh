#!/bin/sh -evx
exec 2> /run/shm/init.log

### set the driver ###
cd /home/pi/RaspberryPiMouse/src/drivers/
make install
sleep 1
chmod 666 /dev/rt*

### motor power off ###
echo 0 > /dev/rtmotoren0
