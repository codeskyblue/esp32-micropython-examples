# 在 PC 上运行此脚本生成 gb2312.bin（用于嵌入式设备读取）
def build_sorted_gb2312_bin(path='gb2312.bin'):
    entries = []

    for high in range(0xB0, 0xF8):  # 高位 B0-F7
        for low in range(0xA1, 0xFF):  # 低位 A1-FE
            gb_bytes = bytes([high, low])
            try:
                char = gb_bytes.decode('gb2312')
                utf8 = char.encode('utf-8')
                if len(utf8) == 3:  # 确保是常规汉字
                    entries.append(utf8 + gb_bytes)  # 组成完整记录：3字节utf8 + 2字节GB2312
            except UnicodeDecodeError:
                continue

    # 按 UTF-8 编码排序（3字节排序）
    entries.sort()

    # 写入二进制文件
    with open(path, 'wb') as f:
        for record in entries:
            f.write(record)

    print(f"✅ 完成：写入 {len(entries)} 条记录到 {path}，共 {len(entries) * 5} 字节")

build_sorted_gb2312_bin()