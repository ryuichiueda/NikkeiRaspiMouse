#!/usr/bin/python
# vim:fileencoding=utf-8

import sys, time, threading
from sensors import Buttons
from actuators import StepMotorPosControl, Leds, Buzzer

class Agent:
    def __init__(self):
        self.state = "init"
        self.motors = StepMotorPosControl()
        self.buttons = Buttons()
        self.buzzer = Buzzer()
        self.leds = Leds()
        #self.camera = PiCamera()
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
                self.loop()
                continue
            elif self.state == "off":
                self.__init()
                sys.exit(0)

            time.sleep(0.1)
    
    def __init(self):
        self.leds.change_all(1,1,1,0)
        self.buzzer.off()
        self.motors.off()
        self.setup()

    def __ready(self):
        self.leds.change_all(1,1,1,1)
        self.buzzer.on(4000)
        self.motors.on()
        self.ready()

    def ready(self):
        pass

    def __reset_check(self):
        while True:
            self.buttons.update()
            if self.buttons.all_pushed_now():
                self.state = "off"
                return
            elif self.buttons.front_pushed():
                self.__state_transition()

    def __state_transition(self):
        if self.state == "init_ok":    self.state = "ready"
        elif self.state == "ready_ok": self.state = "run"
        elif self.state == "run_ok":   self.state = "init"

class AgentHello(Agent):
    def __init__(self):
        Agent.__init__(self)

    def setup(self):
        print >> sys.stderr, "setup"

    def loop(self):
        self.buttons.update()
        if self.buttons.center_pushed():
            self.motors.turn(90)
        elif self.buttons.back_pushed():
            self.motors.turn(-90)

        print "Hello world"

import os,picamera
from sensors import PiCamera

class AgentFileListener(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.opfile = "/run/shm/op"
        self.imagefile = "/var/www/image.jpg"

    def setup(self):
        try:    os.remove(self.opfile)
        except:    pass

    def loop(self):
        try:
            with open(self.opfile,"r") as f:
                op = f.readline().rstrip()

            os.remove(self.opfile)
        except:
            time.sleep(0.01)
            return

        if op == "left":    self.motors.turn(10)
        elif op == "right":    self.motors.turn(-10)
        elif op == "fw":    self.motors.forward(30)
        elif op == "photo":
            self.camera.capture(self.imagefile)
        elif op == "face":
             h = None
             while h == None:
                h = self.camera.face_pos_on_img()

             self.motors.turn(h)

from sensors import Yaw
from actuators import StepMotorRawControl

class AgentGoStraight(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.yaw = Yaw()
        self.motors = StepMotorRawControl()
        self.hz = 0

    def setup(self):
        print >> sys.stderr, "setup"
        self.yaw.off()

    def ready(self):
        print >> sys.stderr, "ready"
        self.yaw.on()
        self.hz = 0

    def loop(self):
        direction = self.yaw.get_value()
        #print direction

        if abs(direction) > 3.0:
            self.hz = 0

        self.hz += 10
        if self.hz > 3500:
            self.hz = 3500

        p_gain = 10.0
        diff = 20*direction / 9 * p_gain
        if diff > 400.0:    diff = 400.0
        elif diff < -400.0: diff = -400.0

        self.motors.output(self.hz + diff, self.hz - diff)

        time.sleep(0.02)
        
if __name__ == '__main__':
    agent = AgentGoStraight()
    agent.do_action()
    
