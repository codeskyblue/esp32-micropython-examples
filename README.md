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
- TODO: GPS模块

# Links
- https://docs.micropython.org/en/latest/
- https://github.com/micropython/micropython-lib
- https://github.com/mcauser/awesome-micropython
- https://docs.geeksman.com/