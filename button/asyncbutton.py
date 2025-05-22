import uasyncio as asyncio
from machine import Pin
import time

class AsyncButton:
    def __init__(self, pin_num, *, check_time=10, debounce_time=50, hold_time=1000):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.check_time = check_time
        self.debounce_time = debounce_time
        self.hold_time = hold_time

        self._was_pressed = False
        self._press_time = 0

    async def run(self):
        while True:
            await self._check_button()
            await asyncio.sleep_ms(self.check_time)

    def _is_pressed(self) -> bool:
        return not self.pin.value() # 低电平触发
    
    def _pressed_ms(self):
        return time.ticks_diff(time.ticks_ms(), self._press_time)

    async def _check_button(self):
        if self._is_pressed():  # 按钮按下（低电平）
            if not self._was_pressed:
                self._was_pressed = True
                self._press_time = time.ticks_ms()
                await asyncio.sleep_ms(self.debounce_time)

                # 检查是否仍按下
                if self._is_pressed():
                    # 等待是否为长按
                    while self._is_pressed():
                        if self._pressed_ms() >= self.hold_time:
                            await self.on_hold()
                            # 等待释放，避免短按也触发
                            while self._is_pressed():
                                await asyncio.sleep_ms(self.check_time)
                            self._was_pressed = False
                            return
                        await asyncio.sleep_ms(self.check_time)
        else:
            if self._was_pressed:
                if self._pressed_ms() < self.hold_time:
                    await self.on_press()
                self._was_pressed = False

    async def on_press(self):
        print("Short press detected.")

    async def on_hold(self):
        print("Long press detected.")