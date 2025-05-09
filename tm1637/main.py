"""
+------------+           
|5         5V| 
|6        GND| -- GND 
|7       3.3V| -- VCC
|8   ESPC3  4| -- DIO
|9          3| -- CLK
|10         2|
|20         1|
|21         0|
+------------+
"""

import time
import tm1637
from machine import Pin

tm = tm1637.TM1637(clk=Pin(3), dio=Pin(4))
tm.show('help')

time.sleep_ms(500)
tm.numbers(12, 34)
time.sleep_ms(200)
tm.numbers(12, 35, colon=False)

# show temperature '24*C'
time.sleep_ms(500)
tm.temperature(24)

# all LEDS off
time.sleep_ms(500)
tm.write([0, 0, 0, 0])