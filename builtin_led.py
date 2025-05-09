# ESP32-C3的板载LED GPIO口是8，低电平开启 (蓝色的)
#
# mpremote run builtin_led.py
#

import time
from machine import Pin

p = Pin(8, Pin.OUT, value=1)
while True:
    p.value(0) # light on
    time.sleep_ms(500)
    p.value(1) # light off
    time.sleep_ms(500)