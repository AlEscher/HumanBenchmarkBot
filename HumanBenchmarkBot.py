from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ctypes import windll
import pynput
import sys
import time

# For the whole bot we access the elements on the webpage, making the use of Python redundant, but wth...


def handleUserInput(userInput, limit):
    """Handles all user input"""
    if (userInput == "help"):
        printHelp(False)
        handleUserInput(input("What next? (Type help for help)\n"), limit)
    elif (len(userInput.split()) == 2 and userInput.split()[0] == "-limit"):
        limitInput = userInput.split()
        if (limitInput[1].isdigit()):
            limit = int(limitInput[1])
        else:
            print("Invalid -limit argument:", limitInput[1])
        handleUserInput(input("What next? (Type help for help)\n"), limit)
    elif (userInput == "quit"):
        print("Goodbye.")
        sys.exit(0)
    else:
        driver.get("https://www.humanbenchmark.com/")
        # 0 -> number_memory 1-> reaction_time 2-> verbal_memory 3-> visual_memory 4-> hearing -> 5-> typing
        testButtons = driver.find_elements_by_class_name("card")

        if (userInput == "number_memory"):
            testButtons[0].click()
            handleNumberMemory(limit)
            handleUserInput(input("What next? (Type help for help)\n"), limit)
        elif(userInput == "reaction_time"):
            testButtons[1].click()
            handleReactionTime(limit)
            handleUserInput(input("What next? (Type help for help)\n"), limit)
        elif (userInput == "verbal_memory"):
            testButtons[2].click()
            handleVerbalMemory(limit)
            handleUserInput(input("What next? (Type help for help)\n"), limit)
        elif (userInput == "visual_memory"):
            testButtons[3].click()
            handleVisualMemory(limit)
            handleUserInput(input("What next? (Type help for help)\n"), limit)
        elif (userInput == "hearing"):
            testButtons[4].click()
            handleHearing()
            handleUserInput(input("What next? (Type help for help)\n"), limit)
        elif (userInput == "typing"):
            testButtons[5].click()
            handleTyping()
            handleUserInput(input("What next? (Type help for help)\n"), limit)
        else:
            print("Unknown test: " + userInput)
            driver.close()
            sys.exit(-1)


def printHelp(isLaunchArgument):
    """Prints a help for this script"""
    if (isLaunchArgument == True):
        print("Usage example: python %s typing" % (sys.argv[0]))
        print("Set an optional limit: %s verbal_memory -limit 100" %
              sys.argv[0])
        print("To print this help: python %s -help" % sys.argv[0])
        print("Available tests:\n- number_memory\n- reaction_time\n- verbal_memory\n- visual_memory\n- hearing\n- typing")
    else:
        print("Write the test you want to start next")
        print("Type help to print this help")
        print("You can set a new limit with: -limit 100")
        print("To exit the program, type quit")
        print("Available tests:\n- number_memory\n- reaction_time\n- verbal_memory\n- visual_memory\n- hearing\n- typing")


def handleNumberMemory(limit):
    wait = 3
    # get and click the start button
    startButton = driver.find_element_by_class_name("hero-button")
    startButton.click()

    for i in range(limit):
        # wait for the number to be shown in order to save it
        number = driver.find_element_by_class_name("big-number").text
        print(number)

        # get the input field, type in the number and press RETURN
        inputFieldPresent = EC.presence_of_element_located(
            # look for a div element of class "test-group" which contains an input element with type "text"
            (By.XPATH, "//div[@class='test-group']//input[@type='text']"))
        try:
            # wait for the input field to become available
            inputField = WebDriverWait(driver, wait).until(inputFieldPresent)
        except TimeoutException:
            print("Timed out while waiting for input field.")
            driver.close()
            sys.exit(-1)
        inputField.send_keys(number)
        inputField.send_keys(Keys.RETURN)
        nextButton = driver.find_element_by_class_name("hero-button")
        nextButton.click()
        # the time the number is displayed increases for each digit added
        wait += 1


def handleReactionTime(limit):
    myMouse = pynput.mouse.Controller()
    dc = windll.user32.GetDC(0)
    gdi = windll.gdi32
    window = driver.find_element_by_css_selector(
        ".test-standard-inner.inner.anim-slide-fade-in")
    x = window.rect["x"] + (window.rect["width"] // 2)
    y = window.rect["y"] + (window.rect["height"] // 2) + 300
    myMouse.position = (x, y)
    # need integers for gdi.GetPixel(x, y)
    x = int(round(x))
    y = int(round(y))
    myMouse.click(pynput.mouse.Button.left, 1)
    num = 0
    while True:
        # different monitors have slightly different values for this green, 7002955 was the green value on my Laptop monitor
        # From what I have found out windll is the fastest way to check a single pixel value (< 10ms)
        if (abs(gdi.GetPixel(dc, x, y) - 7002955) <= 500000 and num < limit):
            myMouse.click(pynput.mouse.Button.left, 1)
            num = num + 1
            print(num)
            time.sleep(0.1)
            # don't click if this was the last run
            if (num != limit):
                myMouse.click(pynput.mouse.Button.left, 1)
            else:
                break


def handleVerbalMemory(limit):
    # get and click the start button
    # don't look for the start button too early...
    time.sleep(1)
    # wait for the start button, as the site can take a second to load for this test
    startButtonPresent = EC.presence_of_element_located(
        (By.CLASS_NAME, "hero-button"))
    try:
        startButton = WebDriverWait(driver, 3).until(startButtonPresent)
    except TimeoutException:
        print("Timed out while waiting for site to load.")
        driver.close()
        sys.exit(-1)
    startButton.click()
    alreadySeen = []

    # keep collecting words and checking if we already saw them
    for i in range(limit):
        currentWord = driver.find_element_by_class_name("word").text
        if (alreadySeen.count(currentWord) > 0):
            driver.find_elements_by_class_name("hero-button")[0].click()
        else:
            alreadySeen.append(currentWord)
            driver.find_elements_by_class_name("hero-button")[1].click()


def handleVisualMemory(limit):
    time.sleep(0.5)
    startButton = driver.find_element_by_class_name("hero-button")
    startButton.click()
    myMouse = pynput.mouse.Controller()
    for i in range(limit):
        whiteSquaresPresent = EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".square.active"))
        try:
            activeSquares = WebDriverWait(driver, 3).until(whiteSquaresPresent)
        except TimeoutException:
            print("Timed out while waiting for white squares to appear.")
            driver.close()
            sys.exit(-1)
        time.sleep(1.5)
        # iterate through all white squares and click on their location
        for square in activeSquares:
            coordinates = (square.rect["x"] + (square.rect["width"] / 2),
                           square.rect["y"] + (square.rect["height"] / 2) + 120)
            myMouse.position = coordinates
            myMouse.click(pynput.mouse.Button.left, 1)
        time.sleep(1)


# the most challenging test of all
def handleHearing():
    time.sleep(0.25)
    driver.find_element_by_class_name("hero-button").click()
    driver.find_element_by_class_name("hero-button").click()
    print("I can hear everything")


def handleTyping():
    time.sleep(0.5)
    textbox = driver.find_element_by_class_name("letters")
    textbox.click()
    myKeyboard = pynput.keyboard.Controller()
    myMouse = pynput.mouse.Controller()
    coordinates = (textbox.rect["x"] + (textbox.rect["width"] / 2),
                   textbox.rect["y"] + (textbox.rect["height"] / 2) + 100)
    textList = []
    textElements = driver.find_elements_by_class_name("incomplete")
    print("Starting to build string...")
    # join all other letters to create a string to type
    # I have no idea why this takes so long
    for textElement in textElements:
        currentChar = textElement.text
        if (currentChar == ""):
            textList.append(" ")
        else:
            textList.append(currentChar)
    text = "".join(textList)
    print("Typing...")
    # pynput's type is more than 10 x faster than
    # textbox.send_keys(text)
    # but the textbox needs to be in focus for pynput
    myMouse.position = coordinates
    myMouse.click(pynput.mouse.Button.left, 1)
    myKeyboard.type(text)


if (len(sys.argv) == 1):
    print("No test specified.")
    printHelp(True)
    sys.exit(0)
elif (len(sys.argv) >= 2 and sys.argv[1] == "-help"):
    printHelp(True)
    sys.exit(0)
else:
    # default limit, can be changed with launch option -limit
    limit = 40
    if (len(sys.argv) == 4 and sys.argv[2] == "-limit"):
        if (sys.argv[3].isdigit()):
            limit = int(sys.argv[3])
        else:
            print("Invalid -limit argument")
            sys.exit(-1)
    options = webdriver.ChromeOptions()
    # specify your Chrome browser location
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    # specify your chromedriver path
    chrome_driver_binary = "C:\\Program Files (x86)\\Google\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(
        executable_path=chrome_driver_binary, options=options)
    print("Starting test: " + sys.argv[1])
    handleUserInput(sys.argv[1], limit)
