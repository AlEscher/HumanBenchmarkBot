from PIL import ImageGrab
from pynput.mouse import Button, Controller
import keyboard
import time
from ctypes import windll

print("Press p to start, default level count is 100")

keyboard.wait("p")

mouse = Controller()

screensize = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
# avoids importing sys
supportedScreenRes = False

# put the whole code in each if statement because apparently bbox doesn't work well with variables...
if (screensize[0] == 1920 and screensize[1] == 1080):
    for x in range(0, 100): 
        image = ImageGrab.grab(bbox=(750, 259, 1150, 659))
        time.sleep(1)
    
        for i in range(0, 400, 10): 
            for j in range(0, 400, 10): 
                if image.getpixel((i, j)) == (255, 255, 255): 
                    mouse.position = (i + 750, j + 259) 
                    mouse.click(Button.left, 1) 

        time.sleep(2)
elif (screensize[0] == 2560 and screensize[1] == 1440):
    for x in range(0, 100): 
        image = ImageGrab.grab(bbox=(1072, 259, 1472, 659))
        time.sleep(1)
    
        for i in range(0, 400, 10): 
            for j in range(0, 400, 10): 
                if image.getpixel((i, j)) == (255, 255, 255): 
                    mouse.position = (i + 1072, j + 259) 
                    mouse.click(Button.left, 1) 

        time.sleep(2)
else:
    print("Sorry, your screen resolution isn't supported.")