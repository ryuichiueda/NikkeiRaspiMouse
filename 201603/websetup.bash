#!/bin/bash -xv
#このファイルのあるディレクトリで実行のこと（手抜き）

#スクリプトを実行可能に
chmod +x -R ./web/ 

#ウェブアプリをコピー。パーミッションも変わる
sudo rsync -av ./web/ /var/www/

#apacheの設定と再起動
sudo cp ./raspimouse.apache2.conf /etc/apache2/sites-available/
sudo rm -f /etc/apache2/sites-enabled/*
sudo ln -s /etc/apache2/sites-available/raspimouse.apache2.conf /etc/apache2/sites-enabled/raspimouse.conf

sudo a2enmod cgi
sudo service apache2 restart
