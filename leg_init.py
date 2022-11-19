from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
f = True # create servos
servos = {}
for i in range(16):
    print(i)
    kit.servo[i].angle=95
    time.sleep(1)
    kit.servo[i].angle=85
    time.sleep(1)
    kit.servo[i].angle=90
    time.sleep(1)
    if f:
        name = input('servo name: ')
        if name != '':
            servos[name] = i
print(servos)