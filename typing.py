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

if (screensize[0] == 1920 and screensize[1] == 1080):
    image = ImageGrab.grab(bbox=(588, 375, 1314, 573))
    myMouse.position = (950, 430)
elif (screensize[0] == 2560 and screensize[1] == 1440):
    image = ImageGrab.grab(bbox=(904, 377, 1634, 575))
    myMouse.position = (1275, 478)
else:
    print("Sorry, your screen resolution isn't supported.")
    sys.exit(1)

if (image != None):
    text = pytesseract.image_to_string(image, lang='eng')
    # tesseract sometimes mistakenly reads "I" as "|"
    text = text.replace("\n", " ").replace("|", "I")
    # click on text feld to focus it
    myMouse.click(pynput.mouse.Button.left, 1)

    print(text)

    myKeyboard.type(text)
