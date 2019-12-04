from PIL import ImageGrab
from pynput.mouse import Button, Controller
import keyboard
import time

mouse = Controller()

imageSet = []

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
