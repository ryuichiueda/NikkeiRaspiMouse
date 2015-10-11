import sys
import threading
import glob

class Sensor:
	def __init__(self):
		self.lock = threading.Lock()

	def update(self):
		with self.lock:
			self._update()
		
	def _readline(self,filename):
		with open(filename,"r") as f:
			return f.readline()


class SensorButtons(Sensor):
#	/dev/rtswitch0: front button
#	/dev/rtswitch1: center button
#	/dev/rtswitch2: rear button

	def __init__(self):
		Sensor.__init__(self)
		self.files = glob.glob("/dev/rtswitch[0-2]")
		self.values = ["1","1","1"]
		self.pushed = [False,False,False]

	def _update(self):
		self.values = map(self._readline,self.files)
		self.pushed = map(lambda v: v == "0",self.values)
		

