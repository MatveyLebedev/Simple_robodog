from __future__ import division
import numpy as np
import pickle
import time
from sympy import Symbol, solve, Eq
import matplotlib.pyplot as plt
from math import floor

class leg:
    @staticmethod
    def inv_angle(ang, inv):
        if inv == -1:
            if ang >= 90:
                l = list(range(90, 181, 1))
                ang = 90 - l.index(ang)
            else:
                l = list(range(90, -1, -1))
                ang = 90 + l.index(ang)
            return ang

    def set_servos(self):
        if self.f_test == False:
            self.kit.servo[self.servos[self.sp1]].angle = self.inv_angle(self.servo_ang_1, self.servo_inv[self.name + '1'])
            self.kit.servo[self.servos[self.sp2]].angle = self.inv_angle(self.servo_ang_2, self.servo_inv[self.name + '2'])
            self.kit.servo[self.servos[self.sp3]].angle = self.inv_angle(self.servo_ang_3, self.servo_inv[self.name + '3'])

    def __init__(self, kit, servos, servo_angles, servo_inv, a0, b0, l0, l1, l2, name, f_test=True):
        self.plot_x = []
        self.plot_y = []
        self.f_test = f_test
        self.kit = kit
        self.servo_angles = servo_angles
        self.servo_inv = servo_inv
        self.servos = servos
        self.name = name
        self.a0 = a0
        self.b0 = b0
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2
        self.y0 = l1 + l2  # change

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
            theta1 = side*(-np.pi/2+np.asin(t5*t8))+np.asin(t5*y)
            theta2 = -np.asin(t14*x)+np.asin(L2*t14*np.sqrt(1/t15*1/t16*t12**2*(-1/4)+1))
            theta3 = -np.pi+np.acos(-t12/2/(L1*L2))

        except ValueError:
            print('ValueError IK')
            error = True
            theta1=90
            theta2=90
            theta3=90

        theta = [theta1, theta2, theta3]
        return (theta, error)

    def move(self, x, y, z=0):
        Start = time.time()

        x = float(x)
        y = float(y)

        theta, error = self.IK(x, y, z)
        a = theta[2]
        b = theta[1]

        """
        d_x = self.leg_solves_x - x
        d_y = self.leg_solves_y - y
        d_xy = d_x**2 + d_y**2
        a, b = np.unravel_index(np.argmin(d_xy), d_xy.shape)
        """

        print('move time: ', time.time() - Start)
        print('a, b: ', a, b)


        self.servo_ang_1 = self.servo_angles[self.name + '1'] + a
        self.servo_ang_2 = self.servo_angles[self.name + '2'] + b
        self.servo_ang_3 = self.servo_angles[self.name + '3']

        print(self.servo_ang_1)
        print(self.servo_ang_2)
        self.plot_x.append(x)
        self.plot_y.append(y)

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
