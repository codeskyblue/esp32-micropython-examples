# hzk16_extractor.py
# 需要文件：HZK16（与此脚本放在同一目录）
import pathlib

FONT_FILENAME = pathlib.Path(__file__).parent.parent / "HZK16S"

def get_gb2312_offset(char):
    """
    获取 GB2312 编码偏移
    """
    gb2312 = char.encode('gb2312')
    area = gb2312[0] - 0xA1
    index = gb2312[1] - 0xA1
    offset = (94 * area + index) * 32
    return offset


def extract_hanzi_dot(char, hzk_file):
    offset = get_gb2312_offset(char)
    hzk_file.seek(offset)
    data = hzk_file.read(32)
    return data

code = """
def draw_text(oled, text, x, y):
    from framebuf import FrameBuffer, MONO_HLSB
    for ch in text:
        pixels = hanzi[ch]
        fb = FrameBuffer(bytearray(pixels), 16, 16, MONO_HLSB)
        oled.blit(fb, x, y)
        x += 16
"""

def main():
    chars = input("请输入中文字符：")
    with open(FONT_FILENAME, "rb") as f:
        print('hanzi = {}')
        for ch in chars:
            dot = extract_hanzi_dot(ch, f)
            print(f"hanzi['{ch}'] = {repr(dot)}")
    print(code)
    print(f"draw_text(oled, '{chars}', 0, 0)")
    print(f"oled.show()")



if __name__ == "__main__":
    main()