from Sensor import Sensor

class SensorButtons(Sensor):
    def __init__(self):
        self.front = "1"
        self.center = "1"
        self.back = "1"
        self.front_pushed = False
        self.center_pushed = False
        self.back_pushed = False

    def update(self):
        with open("/dev/rtswitch0","r") as f:
                self.front = f.readline()
        with open("/dev/rtswitch1","r") as f:
                self.center = f.readline()
        with open("/dev/rtswitch2","r") as f:
                self.back = f.readline()
        
