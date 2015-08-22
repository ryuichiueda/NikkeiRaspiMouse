#!/bin/bash -exv

apt-get install bc
cd /usr/src

git clone https://github.com/raspberrypi/linux || ( cd ./linux && git pull )

cd ./linux

KERNEL=kernel7

make bcm2709_defconfig

make -j4 zImage modules dtbs

make modules_install

cp arch/arm/boot/dts/*.dtb /boot/
cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
cp arch/arm/boot/dts/overlays/README /boot/overlays/
scripts/mkknlimg arch/arm/boot/zImage /boot/$KERNEL.img
