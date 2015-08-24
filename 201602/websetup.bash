#!/bin/bash

sudo apt-get install apache2

chmod +x -R ./web/ 
sudo rsync -av ./web/ /var/www/
sudo cp ./raspimouse.apache2.conf /etc/apache2/sites-available/
sudo rm -f /etc/apache2/sites-enabled/*default*
sudo ln -s /etc/apache2/sites-available/raspimouse.apache2.conf /etc/apache2/sites-enabled/raspimouse.conf
sudo service apache2 restart
