# /usr/bin/python3.7 /home/dog/Simple_robodog/main.py

import time
import pickle
import matplotlib.pyplot as plt
from leg import leg

f_test = False

# constants in mm
l0 = 50
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
    with open('/home/dog/Simple_robodog/colib_coif.pickle', 'rb') as f:
        colibration_coif = pickle.load(f)
    print('coif load')
    print('colib coif: ', colibration_coif)
except FileNotFoundError:
    colibration_coif = {}

try:
    with open('/home/dog/Simple_robodog/servo_inv.pickle', 'rb') as f:
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

FL = leg(kit, servos, servo_angles, servo_inv, a0, b0, l0, l1, l2, 'FL', f_test)
FR = leg(kit, servos, servo_angles, servo_inv, a0, b0, l0, l1, l2, 'FR', f_test)
RL = leg(kit, servos, servo_angles, servo_inv, a0, b0, l0, l1, l2, 'RL', f_test)
RR = leg(kit, servos, servo_angles, servo_inv, a0, b0, l0, l1, l2, 'RR', f_test)


#FL.move(10, 20)

"""
FL.elips_init(1, 1, 1)
for i in range(200):
    FL.elips_step(i / 100)

print(FL.plot_x, FL.plot_y)
plt.scatter(FL.plot_x, FL.plot_y)
plt.show()
"""

# direct move for gagarinskie ctenia
t = 0.8 # time in s
time.sleep(2)
for _ in range(80):
    FL.direct_move(1, 0)
    FR.direct_move(1, 0)
    time.sleep(t / 80)
time.sleep(1)
for _ in range(80):
    RR.direct_move(0, 1, 0)
    time.sleep(t / 80)
time.sleep(3)
for _ in range(80):
    RR.direct_move(0, -1, 0)
    time.sleep(t / 80)

for _ in range(80):
    RL.direct_move(1, 0)
    RR.direct_move(1, 0)
    time.sleep(t / 80)

for _ in range(80):
    FL.direct_move(-1, 0)
    FR.direct_move(-1, 0)
    time.sleep(t / 80 / 2.5)

for _ in range(80):
    RL.direct_move(-1, 0)
    RR.direct_move(-1, 0)
    time.sleep(t / 80 / 2.5)


ang = 50
for _ in range(ang):
    RR.direct_move(0, 0, 1)
    FR.direct_move(0, 0, 1)
    RL.direct_move(0, 0, -1)
    FL.direct_move(0, 0, -1)
    time.sleep(t / ang / 6)

for _ in range(ang):
    RR.direct_move(0, 0, -1)
    FR.direct_move(0, 0, -1)
    RL.direct_move(0, 0, 1)
    FL.direct_move(0, 0, 1)
    time.sleep(t / ang / 6)

for _ in range(ang):
    RR.direct_move(0, 0, -1)
    FR.direct_move(0, 0, -1)
    RL.direct_move(0, 0, 1)
    FL.direct_move(0, 0, 1)
    time.sleep(t / ang / 6)

for _ in range(ang):
    RR.direct_move(0, 0, 1)
    FR.direct_move(0, 0, 1)
    RL.direct_move(0, 0, -1)
    FL.direct_move(0, 0, -1)
    time.sleep(t / ang / 6)









"""
# go
# 1 step
for _ in range(50):
    RR.direct_move(-1, 1)
    FL.direct_move(-1, 1.5)
    time.sleep(t / 50)
# all ff
for _ in range(30):
    RR.direct_move(0, 1)
    FL.direct_move(0, 1)

    RL.direct_move(0, 1)
    FR.direct_move(0, 1)
    time.sleep(t / 30)
# 2 step
"""
