#!/usr/bin/python
# vim:fileencoding=utf-8

import cgi

form = cgi.FieldStorage()

print "Content-type: text/html\n\n"

if not form.has_key("op"):
	print "ERROR"
	sys.exit(1)

try:
	filename = "/run/shm/op"
	with open(filename + ".tmp","w") as f:
		values = form["op"].value
		f.write(values + '\n')
		rename(filename + ".tmp",filename)
except:
	print "FILE ERROR"
