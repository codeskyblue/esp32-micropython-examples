# MicroPython doesn't support __file__ and has limited os.path functionality
GB2312_BIN_PATH = 'gb2312.bin'
HZK16S_PATH = "HZK16S"

# 假设你已保存了 gb2312.bin 并排序
def encode_char(char):
    utf8_bytes = char.encode('utf-8')
    if len(utf8_bytes) != 3:
        # ascii就不用处理了
        return utf8_bytes # b'\xa1\xa1'

    record_size = 5
    with open(GB2312_BIN_PATH, 'rb') as f:
        f.seek(0, 2)
        total_records = f.tell() // record_size
        left = 0
        right = total_records - 1

        while left <= right:
            mid = (left + right) // 2
            f.seek(mid * record_size)
            record = f.read(record_size)
            mid_utf8 = record[:3]

            if utf8_bytes == mid_utf8:
                return record[3:5]
            elif utf8_bytes < mid_utf8:
                right = mid - 1
            else:
                left = mid + 1

    return b'\xa1\xa1' # 空白字符


def encode_string(text):
    result = bytearray()
    for ch in text:
        gb = encode_char(ch)
        result.extend(gb)
    return bytes(result)


def load_hzk16_font(gb_bytes):
    """
    filename需要确保存在
    """
    if len(gb_bytes) != 2:
        raise ValueError("gb_bytes length should=2, got", len(gb_bytes))

    area = gb_bytes[0] - 0xA1
    index = gb_bytes[1] - 0xA1
    offset = (94 * area + index) * 32

    with open(HZK16S_PATH, "rb") as f:
        f.seek(offset)
        return f.read(32)


if __name__ == '__main__':
    # 测试一下
    data = encode_string("Hello世界")
    print(data)
    print('Hello世界'.encode('gb2312'))
    assert data == 'Hello世界'.encode('gb2312')