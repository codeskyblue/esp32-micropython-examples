# Servo 9G经典舵机

其中：9g是这个舵机的重量，非常的常见

9g舵机分为两种

- 第一种可以精准的控制180指向的。
- 第二种是可以360旋转的，但是不能精准指向

我这里目前就研究了180度的舵机

类的定义

```py
class Servo(pin_id,min_us=500.0,max_us=2500.0,min_deg=0.0,max_deg=180.0,freq=50)
```

# Links
- https://github.com/redoxcode/micropython-servo
- https://docs.geeksman.com/esp32/MicroPython/10.esp32-micropython-servo.html