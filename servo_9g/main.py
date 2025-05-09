# coding: utf-8
import time
from servo import Servo

servo = Servo(7) # PWM Pin 7
degrees = [0, 90, 180, 90]

for deg in degrees:
    servo.write(deg)
    time.sleep_ms(500)
