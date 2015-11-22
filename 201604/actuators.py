#!/usr/bin/python
# vim:fileencoding=utf-8
import sys, time, fcntl

class Actuator:
	def __init__(self):
		pass

	def _writeline(self,filename,outstring):
		with open(filename,"w") as f:
			fcntl.flock(f,fcntl.LOCK_EX)
			f.write(outstring)
			fcntl.flock(f,fcntl.LOCK_UN)
			return

class StepMotor(Actuator):
	def __init__(self):
		Actuator.__init__(self)

	def on(self):  self._writeline("/dev/rtmotoren0","1")
	def off(self): self._writeline("/dev/rtmotoren0","0")

class StepMotorRawControl(StepMotor):
	def __init__(self):
		StepMotor.__init__(self)
                self.__l_hz = 0
                self.__r_hz = 0

	def off(self):
            self._writeline("/dev/rtmotor_raw_r0","0")
            self._writeline("/dev/rtmotor_raw_l0","0")
	    self._writeline("/dev/rtmotoren0","0")

        def threshold(self,freq):
            th = 4000
            if freq > th:       return th
            elif freq < -th:    return -th
            else:               return freq

	def output(self,l_hz,r_hz):
            self.__l_hz = self.threshold(l_hz)
            self.__r_hz = self.threshold(r_hz)
	    self._writeline("/dev/rtmotor_raw_r0","%d" % (self.__r_hz))
	    self._writeline("/dev/rtmotor_raw_l0","%d" % (self.__l_hz))

class StepMotorPosControl(StepMotor):
	def __init__(self):
		StepMotor.__init__(self)

	def output(self,l_hz,r_hz,msec):
		self._writeline("/dev/rtmotor0","%d %d %d" % (l_hz,r_hz,msec))

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

