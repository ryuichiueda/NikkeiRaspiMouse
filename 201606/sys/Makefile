install:
	cp robot.sh /etc/init.d/
	chmod +x /etc/init.d/robot.sh
	update-rc.d robot.sh defaults

uninstall:
	rm /etc/init.d/robot.sh
	update-rc.d robot.sh remove
