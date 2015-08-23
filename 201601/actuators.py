#!/usr/bin/python
# vim:fileencoding=utf-8
import sys, time, fcntl

class Actuator:
	def __init__(self):
		pass

	def _writeline(self,filename,outstring):
		with open(filename,"w") as f:
			return self.__writeline_lock(f,outstring)

	def __writeline_lock(self,f,outstring):
		while True:
			try:
				fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)
				print >> f, outstring
				fcntl.flock(f,fcntl.LOCK_UN)
				return
			except: 
				time.sleep(0.001)

class StepMotorPair(Actuator):
	def __init__(self):
		Actuator.__init__(self)
		self.off()

	def output(self,l_hz,r_hz,msec):
		self._writeline("/dev/rtmotor0","%d %d %d" % (l_hz,r_hz,msec))

	def on(self):  self._writeline("/dev/rtmotoren0","1")
	def off(self): self._writeline("/dev/rtmotoren0","0")

	def forward(self,distance):
		r_hz, l_hz = 400, 400
		tm = int(1000*distance/(45*3.141592))
		if tm < 0:
			r_hz, l_hz, tm = -r_hz, -l_hz, -tm

		self.output(l_hz,r_hz,tm)

	def turn(self,deg):
		l_hz, r_hz = -400, 400
		tm = int(1000.0*deg/180)
		if tm < 0:
			r_hz, l_hz, tm = -r_hz, -l_hz, -tm

		self.output(l_hz,r_hz,tm)


class Leds(Actuator):
	def __init__(self):
		Actuator.__init__(self)
		self.change_all(0,0,0,0)

	def change_all(self,leftside,leftfront,rightfront,rightside):
		self._writeline("/dev/rtled0",str(rightside))
		self._writeline("/dev/rtled1",str(rightfront))
		self._writeline("/dev/rtled2",str(leftfront))
		self._writeline("/dev/rtled3",str(leftside))


class Buzzer(Actuator):
	def __init__(self):
		Actuator.__init__(self)
		self.off()

	def on(self,hz): self._writeline("/dev/rtbuzzer0",str(hz))
	def off(self):   self._writeline("/dev/rtbuzzer0","0")

