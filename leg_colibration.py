from adafruit_servokit import ServoKit
import time
import pickle
from leg import leg
inv_angle = leg.inv_angle

kit = ServoKit(channels=16)
# do leg init first
servos = {'RR1': 11, 'RR2': 10, 'RR3': 9, 'RL3': 7, 'RL2': 6, 'RL1': 5, 'FR3': 3, 'FR2': 14,
          'FR1': 1, 'FL2': 1, 'FL3': 2, 'FL1': 0}

try:
    with open('servo_inv.pickle', 'rb') as f:
        servo_inv = pickle.load(f)
    print('coif load')
    print('servo inv: ', servo_inv)
except FileNotFoundError:
    servo_inv = {}
    for name in servos:
        servo_inv[name] = 1


try:
    with open('colib_coif.pickle', 'rb') as f:
        colibration_coif = pickle.load(f)
    print('coif load')
    print('colib coif: ', colibration_coif)
except FileNotFoundError:
    colibration_coif = {}

servo_angles = {}
for n in servos:
    if n in colibration_coif.keys():
        servo_angles[n] = 90 + colibration_coif[n]
    else:
        servo_angles[n] = 90
    kit.servo[servos[n]].angle=inv_angle(servo_angles[n], servo_inv[n])
print(servo_angles)

while True:
    name = input('servo name: ')
    if name == '':
        break
    while True:
        ang = input('angle: ')
        if ang == '':
            break
        elif ang == 'i':
            if servo_inv[name] == 1:
                servo_inv[name] = -1
            else:
                servo_inv[name] = 1
            kit.servo[servos[name]].angle = inv_angle(servo_angles[name], servo_inv[name])
        else:
            if name not in colibration_coif.keys():
                colibration_coif[name] = int(ang)
            colibration_coif[name] += int(ang)
            servo_angles[name] += int(ang) 
            kit.servo[servos[name]].angle = inv_angle(servo_angles[name], servo_inv[name])

print(colibration_coif)
print(servo_inv)

with open('colib_coif.pickle', 'wb') as f:
    pickle.dump(colibration_coif, f)

with open('servo_inv.pickle', 'wb') as f:
    pickle.dump(servo_inv, f)
