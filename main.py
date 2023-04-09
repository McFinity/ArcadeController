import time
import board
import digitalio
import usb_hid
import asyncio
import keypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)

class ArcadeInput:
    def __init__(self, pin, keyboard, keyCode):
        self.pin = pin
        self.keyboard = keyboard
        self.keyCode = keyCode
        
    async def catch_pin_transitions(self):
        with keypad.Keys((self.pin,), value_when_pressed=False) as keys:
            while True:
                event = keys.events.get()
                if event:
                    if event.pressed:
                        self.keyboard.press(self.keyCode)
                    elif event.released:
                        self.keyboard.release(self.keyCode)
                await asyncio.sleep(0)

    def createTask(self):
        return asyncio.create_task(self.catch_pin_transitions())


btnUp = ArcadeInput(board.GP14, keyboard, Keycode.UP_ARROW)
btnDown = ArcadeInput(board.GP15, keyboard, Keycode.DOWN_ARROW)
btnLeft = ArcadeInput(board.GP13, keyboard, Keycode.LEFT_ARROW)
btnRight = ArcadeInput(board.GP12, keyboard, Keycode.RIGHT_ARROW)

btnAux1 = ArcadeInput(board.GP16, keyboard, Keycode.U)
btnAux2 = ArcadeInput(board.GP17, keyboard, Keycode.I)
btnAux3 = ArcadeInput(board.GP18, keyboard, Keycode.O)
btnAux4 = ArcadeInput(board.GP19, keyboard, Keycode.P)

btnA1 = ArcadeInput(board.GP20, keyboard, Keycode.Q)
btnB1 = ArcadeInput(board.GP21, keyboard, Keycode.E)
btnC1 = ArcadeInput(board.GP22, keyboard, Keycode.R)
btnD1 = ArcadeInput(board.GP28, keyboard, Keycode.F)

btnA2 = ArcadeInput(board.GP11, keyboard, Keycode.Z)
btnB2 = ArcadeInput(board.GP10, keyboard, Keycode.X)
btnC2 = ArcadeInput(board.GP9, keyboard, Keycode.C)
btnD2 = ArcadeInput(board.GP8, keyboard, Keycode.V)

async def main():
    await asyncio.gather(
        btnUp.createTask(),
        btnDown.createTask(),
        btnLeft.createTask(),
        btnRight.createTask(),
        btnAux1.createTask(),
        btnAux2.createTask(),
        btnAux3.createTask(),
        btnAux4.createTask(),
        btnA1.createTask(),
        btnB1.createTask(),
        btnC1.createTask(),
        btnD1.createTask(),
        btnA2.createTask(),
        btnB2.createTask(),
        btnC2.createTask(),
        btnD2.createTask()
    )
    
asyncio.run(main())
