import sys, time, threading
from sensors import SensorButtons

class Agent:
	def __init__(self):
		self.thread_reset_check = threading.Thread(target=self.__reset_check)
		self.run = False
		self.pushed = False

	def do_action(self):
		while True:
			if self.pushed:
				self.run = not self.run
				self.pushed = False
				self.thread_reset_check.start()

			if self.run:
				self._one_step()
			else:
				time.sleep(1)
				

	def __reset_check(self):
		while True:
			btns.update()
			if btns.front_pushed():
				self.pushed = True
				return

			sleep(0.1)


class AgentHello(Agent):
	def __init__(self):
		Agent.__init__(self)

	def _one_step(self):
		print "Hello world"
