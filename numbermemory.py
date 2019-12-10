from ctypes import windll
from win32api import GetSystemMetrics
from PIL import ImageGrab
import pynput
import time
import pytesseract
import sys

myKeyboard = pynput.keyboard.Controller()
myMouse = pynput.mouse.Controller()
screensize = windll.user32.GetSystemMetrics(
    0), windll.user32.GetSystemMetrics(1)
# path to tesseract's executable, this should be the standard path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image = None
limit = 5

if (screensize[0] == 1920 and screensize[1] == 1080):
    sys.exit(1)
elif (screensize[0] == 2560 and screensize[1] == 1440):
    myMouse.position = (1273, 574)
    myMouse.click(pynput.mouse.Button.left, 1)
    myMouse.position = (1270, 427)
else:
    print("Sorry, your screen resolution isn't supported.")
    sys.exit(1)

time.sleep(0.2)

for lvl in range(0, limit):
    if (screensize[0] == 1920 and screensize[1] == 1080):
        sys.exit(1)
    elif (screensize[0] == 2560 and screensize[1] == 1440):
        image = ImageGrab.grab(bbox=(1200, 300, 1346, 520))

    if (image is not None):
        #print(pytesseract.image_to_string(image, config='digits'))
        image = image.convert("RGBA")
        pixeldata = image.load()
        #convert the blue background to white and number to black in order to help tesseract recognize the number
        for y in range(0, image.size[1]):
            for x in range(0, image.size[0]):
                if pixeldata[x, y] != (255, 255, 255, 255):
                    pixeldata[x, y] = (250, 250, 250, 255)
                else:
                    pixeldata[x, y] = (0, 0, 0, 255)
        
        number = ""
        if (lvl == 0):
            # supposedly better psm (page segmentation mode) for single digits
            number = pytesseract.image_to_string(image, config='--psm 10')
        else:
            # psm for single word
            number = pytesseract.image_to_string(image, config='--psm 8')
        #try and filter out some consistent mistakes made by tesseract
        number = number.replace("i", "1").replace("&", "6")
        print(number)
        image.show()
        
        if (not number.isdigit()):
            print("Tesseract OCR failed to recognize the number")
            sys.exit(1)
        # click on text feld to focus it
        time.sleep(1)
        myMouse.click(pynput.mouse.Button.left, 1)
        myKeyboard.type(number)
        myKeyboard.press(pynput.keyboard.Key.enter)
        myKeyboard.release(pynput.keyboard.Key.enter)
        time.sleep(0.1)
        myKeyboard.press(pynput.keyboard.Key.enter)
        myKeyboard.release(pynput.keyboard.Key.enter)
        time.sleep(0.5)