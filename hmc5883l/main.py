'''
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
'''


import time
from hmc5883l import HMC5883L

sensor = HMC5883L(scl=0, sda=1)
while 1:
    x, y, z = sensor.read()
    print(x, y, z)
    print('heading:', sensor.heading(x, y))
    time.sleep(.5)