from micropyGPS import MicropyGPS
from machine import RTC, UART
import asyncio
import time
from machine import Pin, I2C
import ssd1306

# using default address 0x3C


class GPS:
    def __init__(self, rx: int, tx: int):
        self.i2c = I2C(scl=Pin(0), sda=Pin(1))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.uart = UART(1, baudrate=9600, rx=tx, tx=rx)
        self.mgps = MicropyGPS()
        self.mgps.local_offset = 8
        self.rtc = RTC()
        self.last_sync_time = 0  # 记录上次同步的时间（以秒计）
    
    async def loop(self):
        while True:
            if self.uart.any():
                data = self.uart.read()
                try:
                    for x in data.decode('utf-8'):
                        self.mgps.update(x)
                except UnicodeError:
                    print("Received:", data)
                    pass
            await asyncio.sleep_ms(10)
    
    async def show(self):
        while True:
            g = self.mgps
            oled = self.oled
            oled.fill(0)
            oled.text(f"course: {g.course}", 0, 0)
            oled.text(f"speed: {g.speed_string()}", 0, 10)
            oled.text(f"sate: {g.satellites_in_use}/{g.satellites_in_view}", 0, 20)
            oled.text(f"time: {g.timestamp[0]:02}:{g.timestamp[1]:02}:{int(g.timestamp[2]):02}", 0, 30)
            oled.show()
            print("Lat:", g.latitude_string())
            print("Lon:", g.longitude_string())
            print("course:", g.course)
            print("speed:", g.speed_string())
            print("Time:", g.date, g.timestamp)
            if self.mgps.satellite_data_updated():
                print("satellite-in-view:", g.satellites_in_view)
                print("satellite-data:", g.satellite_data)
            print("")
            if g.satellites_in_view > 0:
                current_time = time.time()
                if current_time - self.last_sync_time > 3600: # 每1小时尝试同步一次时间
                    self.sync_time_from_gps()
            await asyncio.sleep_ms(1000)

    def sync_time_from_gps(self):
        g = self.mgps
        if g.date and g.timestamp[0] is not None:
            year = 2000 + g.date[2]
            month = g.date[1]
            day = g.date[0]
            hour = g.timestamp[0]
            minute = g.timestamp[1]
            second = int(g.timestamp[2])
            # 设置本地 RTC 时间
            self.rtc.datetime((year, month, day, 0, hour, minute, second, 0))
            self.last_sync_time = time.time()
            print(">>> 本地时间已同步为:", self.rtc.datetime())
            return True
        return False

    async def main(self):
        gps_task = asyncio.create_task(gps.loop())
        show_task = asyncio.create_task(gps.show())
        await asyncio.gather(gps_task, show_task)
        

gps = GPS(20, 21)
asyncio.run(gps.main())
