from PIL import ImageGrab
from ctypes import windll
from win32api import GetSystemMetrics
import pynput
import time
import pytesseract
import sys

myKeyboard = pynput.keyboard.Controller()
myMouse = pynput.mouse.Controller()
screensize = windll.user32.GetSystemMetrics(
    0), windll.user32.GetSystemMetrics(1)
# path to tesseract's executable, this is should be the standard path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image = None
limit = 5

if (screensize[0] == 1920 and screensize[1] == 1080):
    sys.exit(1)
elif (screensize[0] == 2560 and screensize[1] == 1440):
    myMouse.position = (1273, 574)
    myMouse.click(pynput.mouse.Button.left, 1)
    time.sleep(0.2)
    image = ImageGrab.grab(bbox=(12, 335, 2446, 466))
    myMouse.position = (1270, 427)
else:
    print("Sorry, your screen resolution isn't supported.")
    sys.exit(1)
image.show()
# click on text feld to focus it
myMouse.click(pynput.mouse.Button.left, 1)
    
if (image != None):
    for x in range(0, limit):
        time.sleep(1.5)
        if (screensize[0] == 1920 and screensize[1] == 1080):
            sys.exit(1)
        elif (screensize[0] == 2560 and screensize[1] == 1440):
            image = ImageGrab.grab(bbox=(12, 335, 2446, 466))

        number = pytesseract.image_to_string(image)
        print(number)
        myKeyboard.type(number)
        myKeyboard.press(pynput.keyboard.Key.enter)
        myKeyboard.release(pynput.keyboard.Key.enter)
        myKeyboard.press(pynput.keyboard.Key.enter)
        myKeyboard.release(pynput.keyboard.Key.enter)