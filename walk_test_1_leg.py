from Leg_posishon_visualisation import Visualisation_Kit
import pickle
from leg import leg
import numpy as np
import time
import math

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

l0 = 50
l1 = 100
l2 = 135

servos = {'RR1': 2, 'RR2': 1, 'RR3': 0, 'RL3': 4, 'RL2': 5, 'RL1': 6, 'FR3': 15, 'FR2': 14,
          'FR1': 13, 'FL2': 10, 'FL3': 11, 'FL1': 9}

try:
    with open('colib_coif.pickle', 'rb') as f:
        colibration_coif = pickle.load(f)
    print('coif load')
    print('colib coif: ', colibration_coif)
except FileNotFoundError:
    colibration_coif = {}

try:
    with open('servo_inv.pickle', 'rb') as f:
        servo_inv = pickle.load(f)
    print('coif load')
    print('servo inv: ', servo_inv)
except FileNotFoundError:
    servo_inv = {}
    for name in servos:
        servo_inv[name] = 1

servo_angles = {}
for n in servos:
    if n in colibration_coif.keys():
        servo_angles[n] = 90 + colibration_coif[n]
    else:
        servo_angles[n] = 90

v_kit = Visualisation_Kit()

RR = leg(kit, servos, servo_angles, servo_inv, l0, l1, l2,
         name='RR', f_test=False)

scale_X = 0.5
scale_Y = 0.9

T = np.linspace(math.pi, -500*math.pi, 20000)
for t in T:
    
    '''x, y = FR.move_trajectory(t, scale_X=scale_X, scale_Y=scale_Y)
    ang1, ang2 = FR.IK2(x, y)
    ang1 = math.degrees(ang1)
    ang2 = math.degrees(ang2)
    v_kit.set_angle(0, ang1, ang2, x, y)'''
    
    time.sleep(0.005)
    RR.move2(t, scale_X, scale_Y)
    