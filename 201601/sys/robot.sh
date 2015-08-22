#!/bin/sh -evx

cd /run/shm/
exec 2> ./init.log
KODIR=/home/pi/RaspberryPiMouse/src/drivers
DIR=/home/pi/NikkeiRaspiMouse/201601/sys

### set the driver ###
insmod $KODIR/rtmouse.ko
sleep 1
chmod 666 /dev/rt*

### run the main script ###
chmod a+x $DIR/main.bash
sudo -u pi $DIR/main.bash > /dev/null 2> /dev/null &
