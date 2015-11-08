#!/bin/bash -vxe
dir=$(dirname $0)/../

sudo apt-get install apache2

cd $dir

sudo cp ./web/index.html /var/www/html/
