#!/usr/bin/python
# vim:fileencoding=utf-8

import time
import socket

def get_line(s):
    line = ""
    while True:
        v = s.recv(1)
        line += v
        if v == '\n':
            return line
	
def connect():
    while True:
        try :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost",10500))
            return s
        except:
            time.sleep(1.0)


s = connect()
while True: print get_line(s),
