from __future__ import division
import numpy as np
import pickle
import time
from sympy import Symbol, solve, Eq
import matplotlib.pyplot as plt
from math import floor
import math as m

class leg:
    @staticmethod
    def inv_angle(ang, inv):
        ang = int(ang)
        if inv == -1:
            if ang >= 90:
                l = list(range(90, 300, 1))
                ang = 90 - l.index(ang)
            else:
                l = list(range(90, -100, -1))
                ang = 90 + l.index(ang)
        return ang
        
    @staticmethod
    def restr_ang(ang):
        if ang > 180:
            ang = 180
        if ang < 0:
            ang = 0
        return int(ang)

    def set_servos(self):
        if self.f_test == False:
            self.kit.servo[self.sp1].angle = self.restr_ang(self.inv_angle(self.servo_ang_1, self.servo_inv[self.name + '1']))
            self.kit.servo[self.sp2].angle = self.restr_ang(self.inv_angle(self.servo_ang_2, self.servo_inv[self.name + '2']))
            self.kit.servo[self.sp3].angle = self.restr_ang(self.inv_angle(self.servo_ang_3, self.servo_inv[self.name + '3']))

            

    def __init__(self, kit,
                        servos,
                        servo_angles, 
                        servo_inv,
                        l0,
                        l1,
                        l2,
                        name, 
                        f_test):
        self.plot_x = []
        self.plot_y = []
        self.f_test = f_test
        self.kit = kit
        self.servo_angles = servo_angles
        self.servo_inv = servo_inv
        self.servos = servos
        self.name = name
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2
        self.y0 = l1 + l2  # change
        self.R = self.l1*30/44.5
        # Смещение центра окружности 
        self.y0 = -(self.R + self.l1*30/44.5)
        self.x0 = 0
        self.alpha = (m.pi/2-m.asin((self.R - self.l1*30/44.5)/self.R))

        with open('leg_solve_x.pickle', 'rb') as f:
            self.leg_solves_x = pickle.load(f)
        with open('leg_solve_y.pickle', 'rb') as f:
            self.leg_solves_y = pickle.load(f)

        self.sp1 = servos[name + '1']
        self.sp2 = servos[name + '2']
        self.sp3 = servos[name + '3']

        self.servo_ang_1 = servo_angles[name + '1']
        self.servo_ang_2 = servo_angles[name + '2']
        self.servo_ang_3 = servo_angles[name + '3']

        self.set_servos()

    def IK(self, x, y, z):
        L0 = self.l0
        L1 = self.l1
        L2 = self.l2
        side = 1
        d = 0

        t2 = y**2
        t3 = z**2
        t4 = t2+t3
        t5 = 1/np.sqrt(t4)
        t6 = L0**2
        t7 = t2+t3-t6
        t8 = np.sqrt(t7)
        t9 = d - t8
        t10 = x**2
        t11 = t9**2
        t15 = L1**2
        t16 = L2**2
        t12 = t10+t11-t15-t16
        t13 = t10+t11
        t14 = 1/np.sqrt(t13)
        error = False
        try:
            theta1 = side*(-np.pi/2+np.arcsin(t5*t8))+np.arcsin(t5*y)
            theta2 = -np.arcsin(t14*x)+np.arcsin(L2*t14*np.sqrt(1/t15*1/t16*t12**2*(-1/4)+1))
            theta3 = -np.pi+np.arccos(-t12/2/(L1*L2))

        except ValueError:
            print('ValueError IK')
            error = True
            theta1=90
            theta2=90
            theta3=90

        theta = [theta1, theta2, theta3]
        return (theta, error)
    
    def IK2(self, X, Y):
        q2 = m.acos((X**2 + Y**2 - self.l1**2 - self.l2**2)/(2*self.l1*self.l2)) 
        q1 = m.atan2(Y,X) - m.atan2(self.l2*m.sin(q2),(self.l1+self.l2*m.cos(q2)))
        # углы в радианах
        return q1, q2

    def direct_move(self, a, b, g=0):
        self.servo_ang_1 =self.servo_ang_1  + a
        self.servo_ang_2 = self.servo_ang_2 + b
        self.servo_ang_3 = self.servo_ang_3  + g
        self.set_servos()

    def move(self, x, y, z=0):
        Start = time.time()

        x = float(x)
        y = float(y)
        """
        theta, error = self.IK(x, z, y)
        a = int(theta[2])
        b = int(theta[1])

        self.servo_ang_1 = self.servo_angles[self.name + '1'] + a
        self.servo_ang_2 = self.servo_angles[self.name + '2'] + b
        self.servo_ang_3 = self.servo_angles[self.name + '3']
        """

        
        d_x = self.leg_solves_x - x
        d_y = self.leg_solves_y - y
        d_xy = d_x**2 + d_y**2
        a, b = np.unravel_index(np.argmin(d_xy), d_xy.shape)
        
        self.servo_ang_1 = self.servo_angles[self.name + '1'] + a - 90
        self.servo_ang_2 = self.servo_angles[self.name + '2'] + b - 90
        self.servo_ang_3 = self.servo_angles[self.name + '3']

        self.plot_x.append(x)
        self.plot_y.append(y)

        print('move time: ', time.time() - Start)
        print('a, b: ', a, b)
        print(self.servo_ang_1)
        print(self.servo_ang_2)

        self.set_servos()

    def init_pos(self):
        self.servo_ang_1 = self.servo_angles[self.name + '1']
        self.servo_ang_2 = self.servo_angles[self.name + '2']
        self.servo_ang_3 = self.servo_angles[self.name + '3']

        self.set_servos()

    def elips_init(self, coif_a, coif_b, speed):
        self.el_coif_a = coif_a
        self.el_coif_b = coif_b
        self.speed = speed
        self.elips_a = Symbol('a')
        self.elips_b = Symbol('b')
        self.sym_y = Symbol('y')
        self.sym_x = Symbol('x')
        eq_y = Eq((self.sym_y - self.elips_b)**2, self.elips_a**2 - self.sym_x**2 * self.elips_a**2 / self.elips_b**2)
        self.s1, self.s2 = solve(eq_y, self.sym_y)

    def elips_step(self, t,  coif_a=None, coif_b=None, speed=None):  # ep. t = 0.5 is half of sicle
        if coif_a != None: self.el_coif_a = coif_a
        if coif_b != None: self.el_coif_b = coif_b
        if speed != None: self.speed = speed

        S = time.time()

        x = self.speed * np.sin(2 * np.pi * t)
        t = t - floor(t)
        if t >= 0.25 and t <= 0.75:
            y = self.el_coif_a*np.sqrt(self.el_coif_b**2 - x**2)/self.el_coif_b + self.el_coif_b
        else:
            y = -self.el_coif_a*np.sqrt(self.el_coif_b**2 - x**2)/self.el_coif_b + self.el_coif_b
        print(x, y)
        print(time.time() - S)
        self.move(x, y)

    def move_trajectory(self, t, scale_X, scale_Y):
        #t = m.sin(2 * self.rotation_speed * np.pi * t)
        H = self.y0 - 0

        xdef = (self.R * m.cos(t) + self.x0)
        ydef = (self.R * m.sin(t) + self.y0)

        xdef *= scale_X
        ydef *= scale_Y
        H = H*scale_Y
        if ydef < H:
            y = H
        else:
            y = ydef
        x = xdef
        return x, y

    def move_xy(self, x, y):
        ang1, ang2 = self.IK2(x, y)
        ang1 = m.degrees(ang1)
        ang2 = m.degrees(ang2)

        self.servo_ang_1 = self.servo_angles[self.name + '1']
        self.servo_ang_2 = self.servo_angles[self.name + '2'] + ang1 - 180
        self.servo_ang_3 = self.servo_angles[self.name + '3'] + ang2

        self.set_servos()

    def move2(self, t, scale_X, scale_Y):
        x, y = self.move_trajectory(t, scale_X, scale_Y)
        ang1, ang2 = self.IK2(x, y)
        ang1 = m.degrees(ang1)
        ang2 = m.degrees(ang2)

        self.servo_ang_1 = self.servo_angles[self.name + '1']
        self.servo_ang_2 = self.servo_angles[self.name + '2'] + ang1 - 180
        self.servo_ang_3 = self.servo_angles[self.name + '3'] + ang2

        self.set_servos()