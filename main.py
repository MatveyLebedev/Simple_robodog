import time
import pickle
import matplotlib.pyplot as plt
from leg import leg

f_test = False

# constants in mm
l1 = 98
l2 = 126
a0 = 0
b0 = 0

if f_test == False:
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
else:
    kit = None

# do leg init first
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


print(servo_angles)

FL = leg(kit, servos, servo_angles, servo_inv, a0, b0, l1, l2, 'FL', f_test)
FR = leg(kit, servos, servo_angles, servo_inv, a0, b0, l1, l2, 'FR', f_test)
RL = leg(kit, servos, servo_angles, servo_inv, a0, b0, l1, l2, 'RL', f_test)
RR = leg(kit, servos, servo_angles, servo_inv, a0, b0, l1, l2, 'RR', f_test)

"""
FR.move(0, 100)
FL.move(0, 100)
"""

"""
FR.elips_init(5, 5)
for i in range(100):
    FR.elips_step(i / 100)

plt.scatter(FR.plot_x, FR.plot_y)
plt.show()
"""
