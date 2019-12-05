from PIL import ImageGrab
from ctypes import windll
from win32api import GetSystemMetrics
import pynput
import time
import pytesseract

myKeyboard = pynput.keyboard.Controller()
myMouse = pynput.mouse.Controller()
screensize = windll.user32.GetSystemMetrics(
    0), windll.user32.GetSystemMetrics(1)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if (screensize[0] == 1920 and screensize[1] == 1080):
    image = ImageGrab.grab(bbox=(588, 375, 1314, 573))
    text = pytesseract.image_to_string(image, lang='eng')
    # tesseract sometimes mistakenly reads "I" as "|"
    text = text.replace("\n", " ").replace("|", "I")
    # click on text feld to focus it
    myMouse.position = (950, 430)
    myMouse.click(pynput.mouse.Button.left, 1)

    print(text)

    myKeyboard.type(text)

elif (screensize[0] == 2560 and screensize[1] == 1440):
    print("Not yet supported")
else:
    print("Sorry, your screen resolution isn't supported.")
