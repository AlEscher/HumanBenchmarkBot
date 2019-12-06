from PIL import ImageGrab
from pynput.mouse import Button, Controller
import time
from ctypes import windll
import sys

limit = 20
if (len(sys.argv) == 1):
    print("No limit specified, using default of %i" % (limit))
    print("Usage example: python %s 30" % (sys.argv[0]))
elif (sys.argv[1].isdigit()):
    limit = int(sys.argv[1])
else:
    print("Invalid argument.")
    print("Usage example: python %s 30" % (sys.argv[0]))
    sys.exit(1)

mouse = Controller()
image = None
screensize = windll.user32.GetSystemMetrics(
    0), windll.user32.GetSystemMetrics(1)
# can't use variables for width / height, as bbox apparently doesn't work well with variables...
if (screensize[0] == 1920 and screensize[1] == 1080):
    mouse.position = (954, 558)
elif (screensize[0] == 2560 and screensize[1] == 1440):
    mouse.position = (1273, 558)
else:
    print("Sorry, your resolution is not supported.")
    sys.exit(1)

mouse.click(Button.left, 1)
time.sleep(1)

for x in range(0, limit):
    if (screensize[0] == 1920 and screensize[1] == 1080):
        image = ImageGrab.grab(bbox=(750, 259, 1150, 659))
    elif (screensize[0] == 2560 and screensize[1] == 1440):
        image = ImageGrab.grab(bbox=(1072, 259, 1472, 659))

    time.sleep(1.1)

    for i in range(0, 400, 10):
        for j in range(0, 400, 10):
            if image.getpixel((i, j)) == (255, 255, 255):
                if (screensize[0] == 1920 and screensize[1] == 1080):
                    mouse.position = (i + 750, j + 259)
                elif (screensize[0] == 2560 and screensize[1] == 1440):
                    mouse.position = (i + 1072, j + 259)
                mouse.click(Button.left, 1)

    time.sleep(2)
