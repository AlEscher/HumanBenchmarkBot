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
limit = 30

if (screensize[0] == 1920 and screensize[1] == 1080):
    myMouse.position = (953, 574)
    myMouse.click(pynput.mouse.Button.left, 1)
    myMouse.position = (953, 430)
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
        image = ImageGrab.grab(bbox=(540, 340, 1344, 470))
    elif (screensize[0] == 2560 and screensize[1] == 1440):
        image = ImageGrab.grab(bbox=(1000, 300, 1546, 520))

    if (image is not None):
        #print(pytesseract.image_to_string(image, config='digits'))
        image = image.convert("RGBA")
        pixeldata = image.load()
        # convert the blue background to white and number to black in order to help tesseract recognize the number
        for y in range(0, image.size[1]):
            for x in range(0, image.size[0]):
                if pixeldata[x, y] < (250, 250, 250, 255):
                    pixeldata[x, y] = (255, 255, 255, 255)
                else:
                    pixeldata[x, y] = (0, 0, 0, 255)

        number = ""
        if (lvl == 0):
            # supposedly better psm (page segmentation mode) for single characters
            number = pytesseract.image_to_string(image, config='--psm 10')
        else:
            # config for digits
            number = pytesseract.image_to_string(image, config='digits')
        # try and filter out some consistent mistakes made by tesseract
        print("Tesseract read: " + number)
        if (not number.isdigit()):
            number = number.replace("i", "1").replace(
                "&", "6").replace("t", "7").replace("a", "4").replace("G", "6")

        # if (lvl >= 10):
        #     image.show()

        if (not number.isdigit() or len(number) != lvl + 1):
            print("Tesseract OCR failed to recognize the number")
            sys.exit(1)

        print("Writing: " + number)

        delay = 2
        # click on text feld to focus it
        if (lvl >= 2):
            delay += (lvl - 1) * 1
        print("Waiting: " + str(delay) + "s")
        time.sleep(delay)
        myMouse.click(pynput.mouse.Button.left, 1)
        myKeyboard.type(number)
        myKeyboard.press(pynput.keyboard.Key.enter)
        myKeyboard.release(pynput.keyboard.Key.enter)
        time.sleep(0.1)
        myKeyboard.press(pynput.keyboard.Key.enter)
        myKeyboard.release(pynput.keyboard.Key.enter)
        time.sleep(0.5)
