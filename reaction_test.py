from PIL import ImageGrab
from pynput.mouse import Button, Controller
from ctypes import windll
import keyboard

mouse = Controller()

keyboard.wait("p")

mouse.position = (950, 460)
while True:
    # if (pixel == (75, 219, 106)):
    if (windll.gdi32.GetPixel(windll.user32.GetDC(0), 28, 244) == 7002955):
        mouse.click(Button.left, 1)
