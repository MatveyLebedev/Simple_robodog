from Leg_posishon_visualisation import Visualisation_Kit
import pickle
from leg import leg
import numpy as np
import time
import math

l0 = 50
l1 = 100
l2 = 131
servos = {'RR1': 1, 'RR2': 2, 'RR3': 3, 'RL3': 7, 'RL2': 6, 'RL1': 5, 'FR3': 9, 'FR2': 10,
          'FR1': 11, 'FL2': 13, 'FL3': 14, 'FL1': 15}

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

FL = leg(None, servos, servo_angles, servo_inv, l0, l1, l2, 
            rotation_speed=1, name='FL', f_test=True, f_viz=True)

scale_X = 0.8
scale_Y = 1.4

T = np.linspace(math.pi, -50*math.pi, 1000)
for t in T:
    x, y = FL.move_trajectory(t, scale_X=scale_X, scale_Y=scale_Y)
    ang1, ang2 = FL.IK2(x, y)
    ang1 = math.degrees(ang1)
    ang2 = math.degrees(ang2)
    v_kit.set_angle(0, ang1, ang2, x, y)
