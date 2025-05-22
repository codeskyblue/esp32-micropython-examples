# GPS

我用的是大夏龙雀的研发的GPS，定位精度2m
淘宝链接 https://item.taobao.com/item.htm?id=809116697958

默认波特率9600，UART接口

```
    +------------+           
    |5         5V|           
    |6        GND|           
    |7       3.3V|
    |8   ESPC3  4|
    |9          3|
    |10         2|
TX--|20         1|--SDA
RX--|21         0|--SCL
    +------------+
```

```sh
mpremote cp micropyGPS.py :
mpremote cp main.py :
```

# Links
- https://github.com/inmcm/micropyGPS