from machine import RTC, UART, Pin
import time


class BufferReader:
    def __init__(self, reader):
        self.reader = reader
        self.buf = bytearray()
        
    def readline(self) -> bytearray:
        index = self.buf.find(b'\r\n')
        if index != -1:
            line = self.buf[:index]
            self.buf = self.buf[index+2:]
            return line
        self.buf.extend(self.reader.read())
        return self.readline()
    

class GPS():
    def __init__(self, rx: int, tx: int, wake: int):
        self.uart = UART(1, baudrate=9600, rx=rx, tx=tx)
        self.wake_pin = Pin(wake, Pin.OUT) # low to standby
        self.br = BufferReader(self.uart)
    
    def settime(self):
        self.wake_pin.value(1)
        try:
            self._settime()
        except Exception as e:
            print("gps settime failed", e)
        self.wake_pin.value(0)

    def _settime(self):
        while True:
            if not self.uart.any():
                continue
            line = self.br.readline().decode('utf-8')
            if line.startswith('$GNRMC'):
                print('Receive:', line)
                if settime_by_gnrmc(line):
                    return
