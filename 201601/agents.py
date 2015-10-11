import sys, time, threading
from sensors import SensorButtons

class Agent:
	def __init__(self):
		self.run_thread = threading.Thread(target=self._run)

	def run(self):
		try:
			self.run_thread.start()
			__watch_reset()
		except:
			sys.exit(1)

	def __watch_reset(self):
		btns = SensorButtons()
		while True:
			btns.update()
			if btns.front_pushed():
				raise NameError('reset')

			time.sleep(0.1)

class AgentHello(Agent):
	def __init__(self):
		Agent.__init__(self)

	def _run(self):
		print "Hello world"
		time.sleep(5.0)
