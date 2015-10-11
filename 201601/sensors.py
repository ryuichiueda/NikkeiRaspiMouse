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
		self.on_time = [None,None,None]
		self.values = ["1","1","1"]

	def _update(self):
		tm = time.time()
		self.values = map(self._readline,self.files)
		self.on_time = [ tm if v == "0" else past for (v,past) in zip(self.values,self.on_time)]

	def _pushed(self,num):
		if self.on_time[num] == None:
			return False

		THRESHOLD = 0.2
		tm = time.time()
		if tm - self.on_time[num] > THRESHOLD:
			self.on_time[num] = None
			return False
		else:
			return True

	def front_pushed(self):    self._pushed(0)
	def center_pushed(self):   self._pushed(1)
	def back_pushed(self):     self._pushed(2)
