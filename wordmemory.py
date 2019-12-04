from PIL import ImageGrab
from pynput.mouse import Button, Controller
import time
from win32api import GetSystemMetrics

mouse = Controller()
screenWidth = GetSystemMetrics(0)
screenHeight = GetSystemMetrics(1)

imageSet = []

# put the whole code in each if statement because bbox doesn't work well with variables
if (screenWidth == 1920 and screenHeight == 1080):
    for x in range(0, 6):
        alreadySeen = True
        image = ImageGrab.grab(bbox=(766, 396, 1166, 446))
        imageSet.append(image)
        alreadySeen = True
        differentPictures = 0

        for l in range(0, len(imageSet)):
            for i in range(0, 400):
                for j in range(0, 50):
                    if (image.getpixel((i, j)) != imageSet[l].getpixel((i, j))):
                        alreadySeen = False

            if (alreadySeen == False):
                differentPictures = differentPictures + 1

        if (differentPictures < len(imageSet)):
            mouse.position = (871, 502)
        else:
            mouse.position = (1033, 502)

        mouse.click(Button.left, 1)
        time.sleep(2)
elif (screenWidth == 2560 and screenHeight == 1440):
    print("Not yet supported")
else:
    print("Sorry, your screen resolution isn't supported.")

