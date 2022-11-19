import math
import time
from threading import Thread

class walk:
    def __init__(self, FL, FR, RL, RR, l1, l2, steps=20, round_time=5):
        self.FL = FL
        self.FR = FR
        self.RL = RL
        self.RR = RR
        self.l1 = l1
        self.l2 = l2
        self.steps = steps
        self.t = 0
        self.start = time.time()
        self.time_per_step = round_time / steps
        self.tread = None

    def stop(self):
        if self.tread != None:
            self.tread.stop()
        H = self.FL.y0
        self.FL.move_xy(0, H)
        self.FR.move_xy(0, H)
        self.RL.move_xy(0, H)
        self.RR.move_xy(0, H)

    def set_direction(self, scale_X, scale_Y):
        self.scale_X = scale_X
        self.scale_Y = scale_Y

    def walking_loop(self):
        self.start = time.time()
        self.t -= 2*math.pi / self.steps
        self.FL.move2(self.t + math.pi, self.scale_X, self.scale_Y)
        self.FR.move2(self.t, self.scale_X, self.scale_Y)
        self.RL.move2(self.t, self.scale_X, self.scale_Y)
        self.RR.move2(self.t + math.pi, self.scale_X, self.scale_Y)
        spend_time = time.time() - self.start()
        if spend_time < self.time_per_step:
            time.sleep( self.time_per_step - spend_time )

    def go(self):
        self.tread = Thread(target=self.walking_loop)
        self.tread.start()
        