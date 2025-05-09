from framebuf import FrameBuffer, MONO_HLSB
import ssd1306
import gb2312

class ZH_SSD1306_I2C(ssd1306.SSD1306_I2C):
    def text(self, text, x, y, colour=1):
        """ 支持中文
        Args:
            colour: 没啥用
        """
        en_y_off = 4 if any(is_chinese_char(ch) for ch in text) else 0
        for ch in text:
            if is_chinese_char(ch):  # 判断是否是中文
                draw_chinese(self, x, y, ch)
                x += 16  # 中文宽度16像素
            else:
                super().text(ch, x, y+en_y_off, colour)
                x += 8   # 英文字符宽度8像

def is_chinese_char(ch):
    return '\u4e00' <= ch <= '\u9fff'

def draw_chinese(oled, x, y, ch):
    gh_bytes = gb2312.encode_char(ch)
    pixels = gb2312.load_hzk16_font(gh_bytes)
    fb = FrameBuffer(bytearray(pixels), 16, 16, MONO_HLSB)
    oled.blit(fb, x, y)




