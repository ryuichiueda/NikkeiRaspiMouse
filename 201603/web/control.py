#!/usr/bin/python
# vim:fileencoding=utf-8

import cgi,os,time,sys

form = cgi.FieldStorage()
if not form.has_key("op"):
	print "ERROR"
	sys.exit(1)

print "Content-type: text/html\n\n"

img_file = "/var/www/image.jpg"
img_time = 0

try:	img_time = os.stat(img_file).st_mtime
except:	pass

try:
	filename = "/run/shm/op"
	tmp_filename = filename + ".tmp"
	with open(tmp_filename,"w") as f:
		f.write(form["op"].value + '\n')

	os.chmod(tmp_filename,0666)
	os.rename(tmp_filename,filename)

except:
	print "FILE ERROR"

if form["op"].value == "photo":
	while not os.path.exists(img_file):
		pass

	while img_time == os.stat(img_file).st_mtime:
		pass

print form["op"].value
