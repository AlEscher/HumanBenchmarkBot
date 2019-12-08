from PIL import ImageGrab
from pynput.mouse import Button, Controller
from ctypes import windll
import time

mouse = Controller()
dc= windll.user32.GetDC(0)
gdi = windll.gdi32
print("Press Ctrl + C to terminate the program.")

screensize = windll.user32.GetSystemMetrics(
    0), windll.user32.GetSystemMetrics(1)
# avoids importing sys
supportedScreenRes = False
print(windll.gdi32.GetPixel(windll.user32.GetDC(0), 950, 460))

if (screensize[0] == 1920 and screensize[1] == 1080):
    mouse.position = (950, 460)
    supportedScreenRes = True
elif (screensize[0] == 2560 and screensize[1] == 1440):
    mouse.position = (950, 460)
    supportedScreenRes = True
else:
    print("Sorry, your resolution isn't supported.")

# click to start the test
mouse.click(Button.left, 1)

if (supportedScreenRes):
    # we do not specifiy a break condition to maximize performance, program has to be quit with Ctrl + C
    while True:
        # different monitors have slightly different values for this green, 7002955 was the green value on my Laptop monitor
        # From what I have found out windll is the fastest way to check a single pixel value (< 10ms)
        if (abs(gdi.GetPixel(dc, 950, 460) - 7002955) <= 500000):
            mouse.click(Button.left, 1)
            time.sleep(0.1)
            #mouse.click(Button.left, 1)
