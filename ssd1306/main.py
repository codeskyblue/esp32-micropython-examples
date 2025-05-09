# Ref: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
import time
from machine import Pin, I2C
import ssd1306

# using default address 0x3C
i2c = I2C(scl=Pin(0), sda=Pin(1))
print(i2c.scan())
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# coord: 0,0 colour: 1 显示英文字符, 
oled.fill(0)
oled.fill_rect(0, 0, 32, 32, 1)
oled.fill_rect(2, 2, 28, 28, 0)
oled.vline(9, 8, 22, 1)
oled.vline(16, 2, 22, 1)
oled.vline(23, 8, 22, 1)
oled.fill_rect(26, 24, 2, 4, 1)
oled.text('MicroPython', 40, 0, 1)
oled.text('SSD1306', 40, 12, 1)
oled.text('OLED 128x64', 40, 24, 1)
oled.show()

time.sleep(1)
oled.fill(0) # 清空屏幕
# 单行最多16个字母, 8行
for i in range(8):
    oled.text("1234567890123456", 0, i*8, 1)
oled.show()

time.sleep(1)
# 中文显示
from zh_ssd1306 import ZH_SSD1306_I2C
oled = ZH_SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("<<你好世界>>", 0, 0)
oled.show()
