import math
import numpy as np
import matplotlib.pyplot as plt
import time


class Visualisation_Kit:
    def __init__(self, l0 = 50,
                       l1 = 100,
                       l2 = 135
                       ):
        '''
        l1: Длинна лопатки
        l2: Длинна плеча
        l3: Длинна локтя
        '''
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.ax.set_aspect('equal', 'box')
        self.ax.grid()
        self.ax.set_xlim([-100, 100])
        self.ax.set_ylim([-200, 0])

        self.x0 = 0
        self.y0 = 0
        self.z0 = 0
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2
        # 1 not inverse, 2 inverse
        self.inv1 = 1
        self.inv2 = 1
        self.inv3 = 1

    def set_angle(self, angle1, angle2, angle3, x, y):
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)
        angle3 = math.radians(angle3)

        # 1 звено
        x1 = self.l1 * math.cos(angle2)
        y1 = self.l1 * math.sin(angle2)

        # 2 звено 
        x2 = x1 + self.l2 * math.cos(angle2 + angle3)
        y2 = y1 + self.l2 * math.sin(angle2 + angle3)

        X_points = [0, x1, x2]
        Y_points = [0, y1, y2]

        self.l = self.ax.plot(X_points, Y_points)
        self.p = self.ax.scatter(x, y)

        self.fig.canvas.draw()
        renderer = self.fig.canvas.renderer
        self.ax.draw(renderer)
        self.ax.set_aspect('equal', 'box')
        self.ax.grid()
        self.ax.set_xlim([-100, 100])
        self.ax.set_ylim([-200, 0])
        plt.pause(0.001) 
        #print(X_points, Y_points)
        self.ax.clear()

