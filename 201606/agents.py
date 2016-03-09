#!/usr/bin/python
# vim:fileencoding=utf-8

import sys, time, threading
from sensors import Buttons, LightSensors
from actuators import StepMotorPosControl, Leds, Buzzer

class Agent:
    def __init__(self):
        self.state = "init"
        self.motors = StepMotorPosControl()
        self.buttons = Buttons()
        self.lightsensors = LightSensors()
        self.buzzer = Buzzer()
        self.leds = Leds()
        #self.camera = PiCamera()
        threading.Thread(target=self.__reset_check).start()
       # threading.Thread(target=self.__lightsensor_check).start()

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

#    def __lightsensor_check(self):
#        while True:
#            self.lightsensors.update()
#            if self.state == "off":
#                return
#
#            time.sleep(0.02)

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

        if abs(direction) > 5.0:
            self.hz = 0

        self.hz += 10
        if self.hz > 3500:
            self.hz = 3500

        p_gain = 10.0
        diff = 20*direction / 9 * p_gain
        if diff > 400.0:    diff = 400.0
        elif diff < -400.0: diff = -400.0

        self.motors.set_values(self.hz + diff, self.hz - diff)

        time.sleep(0.02)

class AgentRunRandom(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.motors = StepMotorRawControl()
        self.hz = 0

    def setup(self):
        print >> sys.stderr, "setup"

    def ready(self):
        print >> sys.stderr, "ready"
        self.hz = 0

    def loop(self):
        self.hz += 20
        if self.hz > 2500:
            self.hz = 2500

        self.lightsensors.update()
        values = self.lightsensors.get_values()
        [leftfront,leftside,rightside,rightfront] = values

        if leftfront + rightfront > 100:
            self.hz = 0
            self.motors.set_values(0,0)
            time.sleep(0.5)
            if leftfront + leftside > rightfront + rightside:
                self.motors.set_values(300,-300)
            else:
                self.motors.set_values(-300,300)
            time.sleep(0.5)
            return

        if leftside < 50 and rightside < 50:
            self.motors.set_values(self.hz,self.hz)
            time.sleep(0.02)
            return

        #1cm近づくとだいたい50値が増える
        error = (leftside - rightside)/50.0
        #1cmあたり3度/秒変化をつける
        direction = error * 3
        diff = 20*direction / 9

        self.motors.set_values(self.hz + diff, self.hz - diff)
        time.sleep(0.02)

class AgentGoAlongWall(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.motors = StepMotorRawControl()
        self.hz = 0

    def setup(self):
        print >> sys.stderr, "setup"

    def ready(self):
        print >> sys.stderr, "ready"
        self.hz = 0

    def loop(self):
        self.hz += 20
        if self.hz > 2500:
            self.hz = 2500

        self.lightsensors.update()
        values = self.lightsensors.get_values()
        leftside = values[1]

        if leftside < 10:
            self.motors.set_values(self.hz, self.hz)
            time.sleep(0.02)
            return

        target = 200
        #1cm近づくとだいたい50値が増える
        error = (target - leftside)/50.0
        #1cmあたり3度/秒変化をつける
        direction = error * 3
        diff = -20*direction / 9

        self.motors.set_values(self.hz + diff, self.hz - diff)
        time.sleep(0.02)

class AgentStopInFrontOfWall(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.motors = StepMotorRawControl()
        self.hz = 0

    def setup(self):
        print >> sys.stderr, "setup"

    def ready(self):
        print >> sys.stderr, "ready"
        self.hz = 0

    def loop(self):
        self.hz += 20
        if self.hz > 2500:
            self.hz = 2500

        self.lightsensors.update()
        values = self.lightsensors.get_values()
        th = sum(values)

        if th > 100:
            self.hz = 0
            self.motors.set_values(0,0)
            return

        self.motors.set_values(self.hz, self.hz)
        time.sleep(0.02)
        
if __name__ == '__main__':
    agent = AgentFileListener()
    agent.do_action()
    
    
