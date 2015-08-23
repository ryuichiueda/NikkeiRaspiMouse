import time, fcntl, glob, sys

class Sensor:
	def __init__(self):
		pass

	def _readline(self,filename):
		with open(filename,"r") as f:
			while True:
				try:
					fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)
					line = f.readline()
					fcntl.flock(f,fcntl.LOCK_UN)
					return line.rstrip()
				except: 
					time.sleep(0.001)
			
class Buttons(Sensor):

	def __init__(self):
		Sensor.__init__(self)
		self.files = sorted(glob.glob("/dev/rtswitch[0-2]"))
		self.pushed = [False,False,False]
		self.values = ["1","1","1"]

	def update(self):
		self.values = map(self._readline,self.files)
		self.pushed = [ v == "0" or past for (v,past) in zip(self.values,self.pushed)]

	def _check_pushed(self,num):
		if self.values[num] == "0": #now pushing
			return False

		if self.pushed[num]:
			self.pushed[num] = False 
			return True
		else:
			return False

	def front_pushed(self):    return self._check_pushed(0)
	def center_pushed(self):   return self._check_pushed(1)
	def back_pushed(self):     return self._check_pushed(2)
