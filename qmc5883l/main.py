"""
+------------+           
|5         5V|           
|6        GND|           
|7        3.3|
|8   ESPC3  4|
|9          3|
|10         2|
|20         1|--SDA
|21         0|--SCL
+------------+
"""

import time
import math
from qmc5883l import QMC5883L
from machine import I2C, Pin

i2c = I2C(scl=Pin(0), sda=Pin(1))
print(i2c.scan())

sensor = QMC5883L(scl=0, sda=1)
while True:
    x, y, z, _, _ = sensor.read()
    rad = math.atan2(y, x)
    heading = math.degrees(rad)
    print(f'{x}, {y}, {z}, {heading}°')
    time.sleep(.5)