# SSD1306

0.96英寸OLED屏幕，非常的经典，支持I2C


| 参数 | 值 |
| --- | --- |
| 外形尺寸 | 27.5x27.8 mm |
| 玻璃尺寸 | 26.7x19.26x1.4 mm |
| 分辨率 | 128x64 |
| 功耗 | 21mA ~ 28mA |


接口有的是VCC开头，有的是GND开头，用时要看清

英文字母像素: 8x8
汉字: 16x16



# 使用教程

官方的
https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

# 购买链接
https://item.taobao.com/item.htm?id=707427160378

# 驱动安装

```sh
mpremote mip install ssd1306
```

如果要实现中文的显示，稍微有点麻烦，这里用的是HZK16字库，但是因为mp不支持gb2312编码，所以需要自己实现一个

```sh
mpremote cp gb2312.py gb2312.bin HZK16S zh_ssd1306.py :
```

使用的时候

```py
# 中文显示
from zh_ssd1306 import ZH_SSD1306_I2C
i2c = ...
oled = ZH_SSD1306_I2C(128, 64, i2c)
oled.text("<<你好世界>>", 0, 0)
oled.show()
```

如果需要显示的汉字没这么多的话，可以用简单的办法
每个汉字对应16x16的点阵保存到代码里面
使用 [gen_chinese_bytes.py](chinese_scripts/gen_chinese_bytes.py) 来快速生成代码

```sh
$ python chinese_scripts/gen_chinese_bytes.py
请输入中文字符: 
```

# Links
- https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py
- [CSDN 整个好活：micropython utf-8转gb2312](https://blog.csdn.net/jd3096/article/details/130257320)
- [Font字符集](https://github.com/aguegu/BitmapFont)