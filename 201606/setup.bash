#!/bin/bash

apt-get update
apt-get upgrade

apt-get install wpasupplicant
apt-get install openssh-server

apt-get install linux-firmware
apt-get install vim

echo 'deb http://packages.ros.org/ros/ubuntu trusty main' > /etc/apt/sources.list.d/ros-latest.list
apt-get install curl

curl -k https://raw.githubusercontent.com/ros/rosdistro/master/ros.key	|
apt-key add -

apt-get update
apt-get install git
apt-get install ros-indigo-ros-base

rosdep init
rosdep update

sudo apt-get install python-rosinstall

sudo apt-get install make

sudo apt-get install linux-headers-$(uname -r)
