from PIL import ImageGrab
from pynput.mouse import Button, Controller
from timeit import default_timer as timer
import keyboard
import time

keyboard.wait("p")

mouse = Controller()

for x in range(0, 100):
    image = ImageGrab.grab(bbox=(750, 259, 1150, 659))
    time.sleep(1)

    for i in range(0, 400, 10):
        for j in range(0, 400, 10):
            if image.getpixel((i, j)) == (255, 255, 255):
                mouse.position = (i + 750, j + 259)
                mouse.click(Button.left, 1)

    time.sleep(2)
