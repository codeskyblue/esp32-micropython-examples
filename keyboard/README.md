# Keyboard
描述了如何使用ESP32来控制键盘

# Usage

```sh
mpremote cp hid_services.py :
mpremote run keyboard_simple.py
```

这里的Demo实现了Keyboard的模拟，但是音量键的模拟没有成功

代码 consumer_control.py consumer_control_example.py
虽然发送音量+有反应，但是释放没反应，导致音量不停的往上加。

# Links
- https://github.com/Heerkog/MicroPythonBLEHID
- https://usb.org/sites/default/files/hut1_6.pdf

