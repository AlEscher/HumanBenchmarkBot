from PIL import ImageGrab
from pynput.mouse import Button, Controller
import time
from win32api import GetSystemMetrics
import pytesseract
import sys

mouse = Controller()
screenWidth = GetSystemMetrics(0)
screenHeight = GetSystemMetrics(1)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
alreadySeenWords = []
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


# put the whole code in each if statement because bbox doesn't work well with variables...
if (screenWidth == 1920 and screenHeight == 1080):

    # click to start the test
    mouse.position = (956, 618)
    mouse.click(Button.left, 1)

    for x in range(0, limit):
        alreadySeen = False
        # read the current word from the screen
        image = ImageGrab.grab(bbox=(766, 390, 1166, 452))
        # imageName = "screen" + str(x) + ".jpg"
        # image.save(imageName)
        word = pytesseract.image_to_string(image)
        print(word)
        # check if we already saw this word
        for i in range(0, len(alreadySeenWords)):
            if (word == alreadySeenWords[i]):
                alreadySeen = True

        alreadySeenWords.append(word)

        if (alreadySeen):
            mouse.position = (871, 502)
        else:
            mouse.position = (1033, 502)

        mouse.click(Button.left, 1)
        time.sleep(0.2)
elif (screenWidth == 2560 and screenHeight == 1440):
    for x in range(0, limit):
        alreadySeen = False
        image = ImageGrab.grab(bbox=(973, 373, 1582, 473))
        word = pytesseract.image_to_string(image, lang='eng')
        print(word)

        for i in range(0, len(alreadySeenWords)):
            if (word == alreadySeenWords[i]):
                alreadySeen = True

        alreadySeenWords.append(word)

        if (alreadySeen):
            mouse.position = (1193, 507)
        else:
            mouse.position = (1357, 507)

        mouse.click(Button.left, 1)
        time.sleep(0.2)
else:
    print("Sorry, your screen resolution isn't supported.")
