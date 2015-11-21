#!/bin/sh -evx
exec 2> /run/shm/init.log

### set the driver ###
insmod /home/pi/RaspberryPiMouse/src/drivers/rtmouse.ko ||
insmod /home/pi/RaspberryPiMouse/lib/Pi2B+/$(uname -r)/rtmouse.ko
sleep 1
chmod 666 /dev/rt*

### motor power off ###
echo 0 > /dev/rtmotoren0

###スティッキービットの解除###
sudo chmod o-t /run/shm/
