#!/usr/bin/python
# vim:fileencoding=utf-8

import socket

def get_line(s):
	line = ""
	while True:
		v = s.recv(1)
		line += v
		if v == '\n':
			return line


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost",10500))

def put_op(command):
	filename = "/run/shm/op"
	tmp_filename = filename + ".tmp"
	with open(tmp_filename,"w") as f:
		f.write(command + '\n')

	os.chmod(tmp_filename,0666)
	os.rename(tmp_filename,filename)

while True:
	line = get_line(s)
	if '前' in line: put_op('fw')
	if '左' in line: put_op('left')
	if '右' in line: put_op('right')
