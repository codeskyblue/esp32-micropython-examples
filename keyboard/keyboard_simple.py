import uasyncio as asyncio
from machine import Pin
from hid_services import Keyboard

# HID keyboard scan codes
KEYCODES = {}

# Add lowercase letters (a-z, no shift)
for i in range(26):
    KEYCODES[chr(ord('a') + i)] = (0, 0x04 + i)
    KEYCODES[chr(ord('A') + i)] = (1, 0x04 + i)

# Add numbers (0-9, no shift)
for i in range(10):
    KEYCODES[str(i)] = (0, 0x1E + i)

# Add other keys
KEYCODES.update({
    # Symbols with shift (number row)
    '!': (1, 0x1E),  # Shift + 1
    '@': (1, 0x1F),  # Shift + 2
    '#': (1, 0x20),  # Shift + 3
    '$': (1, 0x21),  # Shift + 4
    '%': (1, 0x22),  # Shift + 5
    '^': (1, 0x23),  # Shift + 6
    '&': (1, 0x24),  # Shift + 7
    '*': (1, 0x25),  # Shift + 8
    '(': (1, 0x26),  # Shift + 9
    ')': (1, 0x27),  # Shift + 0

    # Common symbols without shift
    ' ': (0, 0x2C),  # Space
    '-': (0, 0x2D),  # Minus
    '=': (0, 0x2E),  # Equals
    '[': (0, 0x2F),  # Left bracket
    ']': (0, 0x30),  # Right bracket
    '\\': (0, 0x31),  # Backslash
    ';': (0, 0x33),  # Semicolon
    "'": (0, 0x34),  # Quote
    '`': (0, 0x35),  # Backtick
    ',': (0, 0x36),  # Comma
    '.': (0, 0x37),  # Period
    '/': (0, 0x38),  # Forward slash

    # Symbols with shift
    '_': (1, 0x2D),  # Shift + -
    '+': (1, 0x2E),  # Shift + =
    '{': (1, 0x2F),  # Shift + [
    '}': (1, 0x30),  # Shift + ]
    '|': (1, 0x31),  # Shift + \
    ':': (1, 0x33),  # Shift + ;
    '"': (1, 0x34),  # Shift + '
    '~': (1, 0x35),  # Shift + `
    '<': (1, 0x36),  # Shift + ,
    '>': (1, 0x37),  # Shift + .
    '?': (1, 0x38),  # Shift + /

    # Special keys
    '\n': (0, 0x28),  # Enter/Return
})

pin_boot = Pin(9, Pin.IN, Pin.PULL_UP)#, Pin.PULL_UP)

class MyKeyboard:
    def __init__(self, name: str):
        self.keyboard = Keyboard(name)
        self.keyboard.start()
        self.keyboard.start_advertising()

    async def run(self):
        while True:
            await self._loop()
    
    async def _loop(self):
        if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
            if await self.is_pressed():
                print("Boot Key pressed", self.is_pressed())
                await self.send_string("Hello world\n")
        
        if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
            await asyncio.sleep_ms(50)
        elif self.keyboard.get_state() is Keyboard.DEVICE_IDLE:
            self.keyboard.start_advertising()
            await asyncio.sleep_ms(50)
        else:
            await asyncio.sleep(1)

    async def is_pressed(self):
        if not pin_boot.value(): # pressed
            await asyncio.sleep_ms(50)
            if not pin_boot.value():
                return True
        return False

    async def send_string(self, st):
        for c in st:
            print("send:", repr(c))
            await self.send_char(c)

    async def send_char(self, char):
        # Special case for space to keep the print message
        if char in KEYCODES:
            mod, code = KEYCODES[char]
        else:
            assert 0, f'invalid char: {repr(char)}'
        await self._send_key(mod, code)
    
    async def _send_key(self, mod, code):
        self.keyboard.set_keys(code)
        self.keyboard.set_modifiers(left_shift=mod)
        await self._safe_notify_hid_report()
        await asyncio.sleep_ms(2)

        self.keyboard.set_keys()
        self.keyboard.set_modifiers()
        await self._safe_notify_hid_report()
        await asyncio.sleep_ms(2)


    async def _safe_notify_hid_report(self):
        try:
            self.keyboard.notify_hid_report()
        except OSError as e:
            if e.args[0] == 12:  # ENOMEM
                print("⚠️ BLE缓存区满，稍后重试")
                await asyncio.sleep_ms(100)  # 休息后重试

async def main():
    kbd = MyKeyboard("BLE Keyboard2")
    await kbd.run()

asyncio.run(main())