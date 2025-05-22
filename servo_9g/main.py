# coding: utf-8
import time
from servo import Servo

servo = Servo(21) # PWM Pin 7
degrees = [0, 90, 180, 90]

for deg in degrees:
    servo.write(deg)
    print("Degree:", deg)
    time.sleep(1)

servo.write(0)