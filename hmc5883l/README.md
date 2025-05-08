# HMC5883L

XYZ的值变化看起来正常，但是计算磁方位角的时候，就不对了。
Y值没有出现正值，导致atan2计算出来的角度也不对。

购买链接
https://detail.tmall.com/item.htm?id=676370039176

分类：HMC5883L GY-271

```py
from hmc5883l import HMC5883L

sensor = HMC5883L(scl=4, sda=5)

x, y, z = sensor.read()
print(sensor.format_result(x, y, z))
```



# Links
- https://github.com/gvalkov/micropython-esp8266-hmc5883l/blob/main/hmc5883l.py
- https://github.com/peppe8o/rpi-pico-peppe8o/blob/main/libraries/hmc5883l.py
- https://github.com/ArcadiaLabs/python_libs/blob/master/i2c/i2c_hmc5883l.py

其实这些代码都差不多