from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

time.sleep(0.1)
kit.servo[1].angle=90
print(i)
