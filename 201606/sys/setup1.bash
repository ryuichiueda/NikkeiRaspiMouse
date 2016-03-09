#!/bin/bash -e

apt-get install alsa-utils

touch /etc/modprobe.d/alsa-base.conf
mv /etc/modprobe.d/alsa-base.conf /etc/modprobe.d/alsa-base.conf.org

cp ./alsa-base.conf /etc/modprobe.d/alsa-base.conf

sudo reboot
