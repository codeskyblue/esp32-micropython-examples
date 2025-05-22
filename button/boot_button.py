from asyncbutton import AsyncButton
import asyncio

class MyButton(AsyncButton):
    async def on_press(self):
        print(">>> You tapped the button!")

    async def on_hold(self):
        print(">>> You held the button!")

async def main():
    btn = MyButton(9)
    await btn.run()

asyncio.run(main())