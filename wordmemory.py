from PIL import ImageGrab
from pynput.mouse import Button, Controller
import time
from win32api import GetSystemMetrics
import pytesseract
import sys

mouse = Controller()
screenWidth = GetSystemMetrics(0)
screenHeight = GetSystemMetrics(1)
# path to tesseract's executable, this is should be the standard path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
alreadySeenWords = []
limit = 20
image = None

if (len(sys.argv) == 1):
    print("No limit specified, using default of %i" % (limit))
    print("Usage example: python %s 30" % (sys.argv[0]))
elif (sys.argv[1].isdigit()):
    limit = int(sys.argv[1])
else:
    print("Invalid argument.")
    print("Usage example: python %s 30" % (sys.argv[0]))
    sys.exit(1)


# can't use variables for width / height, as bbox apparently doesn't work well with variables...
if (screenWidth == 1920 and screenHeight == 1080):
    # click to start the test
    mouse.position = (956, 618)
elif (screenWidth == 2560 and screenHeight == 1440):
    # click to start the test
    mouse.position = (1263, 615)
else:
    print("Sorry, your screen resolution isn't supported.")
    sys.exit(1)
    
mouse.click(Button.left, 1)
time.sleep(0.1)

for x in range(0, limit):
    alreadySeen = False
    # read the current word from the screen
    if (screenWidth == 1920 and screenHeight == 1080):
        image = ImageGrab.grab(bbox=(766, 390, 1166, 452))
    elif (screenWidth == 2560 and screenHeight == 1440):
        image = ImageGrab.grab(bbox=(973, 373, 1582, 473))

    if (image == None):
        sys.exit(-1)

    # imageName = "screen" + str(x) + ".jpg"
    # image.save(imageName)
    word = pytesseract.image_to_string(image)
    print(word)
    # check if we already saw this word
    for i in range(0, len(alreadySeenWords)):
        if (word == alreadySeenWords[i]):
            alreadySeen = True

    alreadySeenWords.append(word)

    if (screenWidth == 1920 and screenHeight == 1080):
        if (alreadySeen):
            mouse.position = (871, 502)
        else:
            mouse.position = (1033, 502)
    elif (screenWidth == 2560 and screenHeight == 1440):
        if (alreadySeen):
            mouse.position = (1193, 507)
        else:
            mouse.position = (1357, 507)

    mouse.click(Button.left, 1)
    time.sleep(0.2)
