# esp32-micropython-examples
经过我自己实践的esp32 micropython例子程序

# 烧录工具

下面这个比较简单，能自动识别型号，选择相应的固件。

使用Edge浏览器打开 <https://dev.16302.com/tools/deviceinit>

引脚图

```
+------------+           
|5         5V|           
|6        GND|           
|7       3.3V|
|8   ESPC3  4|
|9          3|
|10         2|
|20         1|
|21         0|
+------------+

GPIO-8: 板载LED (低电平开启)
GPIO-9: Boot按钮 （低电平触发）
```

# Examples

- [qmc5883l](qmc5883l) 国产罗盘模块
- [hmc5008l](hmc5883l) 进口罗盘模块
- [板载LED控制](builtin_led.py)
- [SSD1306](ssd1306) 0.96英寸OLED屏幕 （阳光下看不清楚） 已经搞定中文显示
- [TM1637 4位数码管](tm1637)
- [SG90 9G经典舵机](servo_9g)
- [mpu6050](mpu6050) 6轴陀螺仪
- [GPS模块](gps)
- [button](button) 按钮（todo）


# 如何擦除固件

```sh
$ python -m serial.tools.list_ports
/dev/cu.Bluetooth-Incoming-Port
/dev/cu.MT810-F3C5
/dev/cu.usbserial-0001

$ esptool.py --port /dev/cu.usbserial-0001 erase_flash
esptool.py v4.7.0
Serial port /dev/cu.usbserial-0001
Connecting.......
Detecting chip type... Unsupported detection protocol, switching and trying again...
Connecting.........
Detecting chip type... ESP32
Chip is ESP32-D0WD-V3 (revision v3.1)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 88:13:bf:0d:32:78
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 0.0s
Hard resetting via RTS pin...
```


# Links
- https://docs.micropython.org/en/latest/
- https://github.com/micropython/micropython-lib
- https://github.com/mcauser/awesome-micropython
- https://docs.geeksman.com/