import sys
import threading
import glob
import time

class Sensor:
	def __init__(self):
		self.lock = threading.Lock()

	def update(self):
		with self.lock:
			self._update()
		
	def _readline(self,filename):
		with open(filename,"r") as f:
			return f.readline().rstrip()


class SensorButtons(Sensor):
	def __init__(self):
		Sensor.__init__(self)
		self.files = sorted(glob.glob("/dev/rtswitch[0-2]"))
		self.pushed = [None,None,None]
		self.values = ["1","1","1"]

	def _update(self):
		tm = time.time()
		self.values = map(self._readline,self.files)
		self.pushed = [ v == "0" or past for (v,past) in zip(self.values,self.pushed)]

	def _pushed(self,num):
		if self.on_time[num] == None:
			return False

		self.on_time[num] = None
		return True

	def front_pushed(self):    self._pushed(0)
	def center_pushed(self):   self._pushed(1)
	def back_pushed(self):     self._pushed(2)
