#!/usr/bin/python
# vim:fileencoding=utf-8
import sys, time, threading
from sensors import Buttons
from actuators import StepMotorPair, Leds, Buzzer

class Agent:
	def __init__(self):
		self.state = "init"
		self.motors = StepMotorPair()
		self.buttons = Buttons()
		self.buzzer = Buzzer()
		self.leds = Leds()
		threading.Thread(target=self.__reset_check).start()

	def do_action(self):
		while True:
			if self.state == "init":
				self.__init()
				self.state = "init_ok"
			elif self.state == "ready":
				self.__ready()
				self.state = "ready_ok"
			elif self.state == "run":
				self.leds.change_all(0,0,0,0)
				self.buzzer.off()
				self.state = "run_ok"
			elif self.state == "run_ok":
				self.one_step()
				continue
			elif self.state == "off":
				self.__init()
				sys.exit(0)

			time.sleep(0.1)
	
	def __init(self):
		self.leds.change_all(1,1,1,0)
		self.buzzer.off()
		self.motors.off()
		self.init()

	def __ready(self):
		self.leds.change_all(1,1,1,1)
		self.buzzer.on(4000)
		self.motors.on()

	def __reset_check(self):
		while True:
			self.buttons.update()
			if self.buttons.all_pushed_now():
				self.state = "off"
				return
			elif self.buttons.front_pushed():
				self.__state_transition()

			time.sleep(0.1)

	def __state_transition(self):
		if self.state == "init_ok":    self.state = "ready"
		elif self.state == "ready_ok": self.state = "run"
		elif self.state == "run_ok":   self.state = "init"

class AgentHello(Agent):
	def __init__(self):
		Agent.__init__(self)

	def init(self):
		pass

	def one_step(self):
		self.buttons.update()
		if self.buttons.center_pushed():
			self.motors.turn(90)
		elif self.buttons.back_pushed():
			self.motors.turn(-90)

		print "Hello world"
