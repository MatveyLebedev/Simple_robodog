# /usr/bin/python3.7 /home/dog/Simple_robodog/main.py

import time
import pickle
import matplotlib.pyplot as plt
from leg import leg
from walk import walk

f_test = True

# constants in mm
l0 = 50
l1 = 100
l2 = 135
a0 = 0
b0 = 0

if f_test == False:
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
else:
    kit = None

# do leg init first
servos = {'RR1': 2, 'RR2': 1, 'RR3': 0, 'RL3': 4, 'RL2': 5, 'RL1': 6, 'FR3': 15, 'FR2': 14,
          'FR1': 13, 'FL2': 10, 'FL3': 11, 'FL1': 9}

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

FL = leg(kit, servos, servo_angles, servo_inv, l0, l1, l2, 'FL', f_test, x0_shift=-75, y0_shift=7)
FR = leg(kit, servos, servo_angles, servo_inv, l0, l1, l2, 'FR', f_test, x0_shift=-75, y0_shift=7)
RL = leg(kit, servos, servo_angles, servo_inv, l0, l1, l2, 'RL', f_test, x0_shift=-150)
RR = leg(kit, servos, servo_angles, servo_inv, l0, l1, l2, 'RR', f_test, x0_shift=-150)


Walk_controller = walk(FL, FR, RL, RR, l1, l2, steps=20, round_time=5)

Walk_controller.stop()
time.sleep(2)
#Walk_controller.shag_go(1)

Walk_controller.simple_go(10)

Walk_controller.stop()

















#FL.move(10, 20)

"""
FL.elips_init(1, 1, 1)
for i in range(200):
    FL.elips_step(i / 100)
git config --global user.email "you@example.com"
print(FL.plot_x, FL.plot_y)
plt.scatter(FL.plot_x, FL.plot_y)
plt.show()
"""
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
servos = {'RR1': 2, 'RR2': 1, 'RR3': 0, 'RL3': 4, 'RL2': 5, 'RL1': 6, 'FR3': 15, 'FR2': 14,
          'FR1': 13, 'FL2': 10, 'FL3': 11, 'FL1': 9}