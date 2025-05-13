import uasyncio as asyncio
from machine import Pin
from consumer_control import ConsumerControl

# Use the BOOT button on ESP32 (GPIO 0)
pin_boot = Pin(9, Pin.IN, Pin.PULL_UP)

class MediaController:
    def __init__(self, name: str):
        self.controller = ConsumerControl(name)
        self.controller.start()

    async def run(self):
        while True:
            await self._loop()
    
    async def _loop(self):
        if self.controller.get_state() is ConsumerControl.DEVICE_CONNECTED:
            if await self.is_pressed():
                print("Boot Key pressed")
                # Send volume up command
                self.controller.volume_up()
                # Wait to avoid multiple presses
                await asyncio.sleep_ms(300)
        
        if self.controller.get_state() is ConsumerControl.DEVICE_CONNECTED:
            await asyncio.sleep_ms(50)
        elif self.controller.get_state() is ConsumerControl.DEVICE_IDLE:
            try:
                self.controller.start_advertising()
            except OSError as e:
                print(f"Error starting advertising: {e}")
            await asyncio.sleep_ms(50)
        else:
            await asyncio.sleep(1)

    async def is_pressed(self):
        if not pin_boot.value():  # pressed
            await asyncio.sleep_ms(50)  # debounce
            if not pin_boot.value():
                return True
        return False

async def main():
    controller = MediaController("BLE Controller")
    await controller.run()

# Run the main function
asyncio.run(main())
