from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as seleniumexcept
from ctypes import windll
import pynput
import sys
import time

# For the whole bot we access the elements on the webpage, making the use of Python redundant, but wth...


def handleUserInput(userInput, limit, fast):
    """Handles all user input"""
    if (userInput is None):
        driver.get("https://www.humanbenchmark.com/")
    elif (userInput == "help"):
        printHelp(False)
    elif (len(userInput.split()) == 2 and userInput.split()[0] == "-limit"):
        limitInput = userInput.split()
        if (limitInput[1].isdigit() and (int(limitInput[1]) > 0)):
            limit = int(limitInput[1])
            print("> Changed limit to:", str(limit))
        else:
            print("> Invalid -limit argument:", limitInput[1])
    elif (userInput == "fast"):
        fast = True
        print("> Changed to fast")
    elif (userInput == "stable"):
        fast = False
        print("> Changed to stable")
    elif (userInput == "quit"):
        print("> Goodbye.")
        sys.exit(0)
    elif (userInput == "close"):
        print("> Goodbye.")
        try:
            driver.close()
            sys.exit(0)
        # raised if the browser is already closed
        except seleniumexcept.WebDriverException:
            sys.exit(0)
    else:
        driver.get("https://www.humanbenchmark.com/")
        # 0 -> number_memory 1-> reaction_time 2-> verbal_memory 3-> visual_memory 4-> hearing -> 5-> typing
        testButtons = driver.find_elements_by_class_name("card")

        if (userInput == "number_memory"):
            testButtons[0].click()
            handleNumberMemory(limit)
        elif(userInput == "reaction_time"):
            testButtons[1].click()
            handleReactionTime(limit)
        elif (userInput == "verbal_memory"):
            testButtons[2].click()
            handleVerbalMemory(limit)
        elif (userInput == "visual_memory"):
            testButtons[3].click()
            if (fast):
                handleVisualMemoryFast(limit)
            else:
                handleVisualMemoryStable(limit)
        elif (userInput == "hearing"):
            testButtons[4].click()
            handleHearing()
        elif (userInput == "typing"):
            testButtons[5].click()
            handleTyping()
        else:
            print("> Unknown test: " + userInput)
    handleUserInput(
        input("\n> What next? (Type help for help)\n# "), limit, fast)


def printHelp(isLaunchArgument):
    """Prints a help for this script, depending on the way "help" was called"""
    if (isLaunchArgument):
        print("Usage example: python %s typing" % (sys.argv[0]))
        print("Set an optional limit: %s verbal_memory -limit 100" %
              sys.argv[0])
        print("To print this help: python %s -help" % sys.argv[0])
        print("Available tests:\n- number_memory\n- reaction_time\n- verbal_memory\n- visual_memory\n- hearing\n- typing")
    else:
        print("> Available commands:")
        print("\t- 'quit' : Terminates this program")
        print("\t- 'close' : Terminates this program and closes the browser")
        print("\t- 'help' : Prints this help")
        print("\t- '-limit x': Sets the limit to x")
        print("\t- 'fast' / 'stable' : Switch between fast and stable execution of the next test")
        print("\t- 'testname' : Starts the test \"testname\"")
        print("> Available tests:\n\t- number_memory\n\t- reaction_time\n\t- verbal_memory\n\t- visual_memory (fast / stable)\n\t- hearing\n\t- typing")


def handleNumberMemory(limit):
    wait = 3
    # get and click the start button
    startButton = driver.find_element_by_class_name("hero-button")
    startButton.click()

    for i in range(limit):
        # save the current number
        number = driver.find_element_by_class_name("big-number").text

        # wait for and get the input field, type in the number and press RETURN
        inputFieldPresent = EC.presence_of_element_located(
            # look for a div element of class "test-group" which contains an input element with type "text"
            (By.XPATH, "//div[@class='test-group']//input[@type='text']"))
        try:
            # wait for the input field to become selectable,  with 'wait' as our max waiting time
            inputField = WebDriverWait(driver, wait).until(inputFieldPresent)
        except TimeoutException:
            print("> Timed out while waiting for input field.")
            driver.close()
            sys.exit(-1)
        inputField.send_keys(number)
        inputField.send_keys(Keys.RETURN)
        nextButton = driver.find_element_by_class_name("hero-button")
        nextButton.click()
        # the time the number is displayed for increases for each digit added
        wait += 1


def handleReactionTime(limit):
    myMouse = pynput.mouse.Controller()
    dc = windll.user32.GetDC(0)
    gdi = windll.gdi32
    # the center of the green / red window
    window = driver.find_element_by_css_selector(
        ".test-standard-inner.inner.anim-slide-fade-in")
    x = window.rect["x"] + (window.rect["width"] // 2)
    y = window.rect["y"] + (window.rect["height"] // 2) + 100
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
            # give the browser time to change the color of the window from green to blue, or else the bot might click twice
            time.sleep(0.1)
            try:
                timeDisplay = driver.find_element_by_xpath(
                    "/html/body/div/div/div[4]/div[1]/div/div[1]/h1/div")
                print("> Took", timeDisplay.text)
            except seleniumexcept.NoSuchElementException:
                print("> Couldn't find time display, maybe the absolute XPath changed?")
            # don't click next if this was the last run
            if (num != limit):
                myMouse.click(pynput.mouse.Button.left, 1)
            else:
                break


def handleVerbalMemory(limit):
    # get and click the start button
    # wait for the start button, as the site can take a second to load for this test
    startButtonPresent = EC.element_to_be_clickable(
        (By.CLASS_NAME, "hero-button"))
    try:
        startButton = WebDriverWait(driver, 3).until(startButtonPresent)
    except TimeoutException:
        print("> Timed out while waiting for site to load.")
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


def handleVisualMemoryStable(limit):
    """More stable version of handleVisualMemory
    The browser doesn't need to be maximised, scrolled to the top or even opened
    for this version to work. Doesn't grab your mouse"""
    startButtonPresent = EC.element_to_be_clickable(
        (By.CLASS_NAME, "hero-button"))
    try:
        startButton = WebDriverWait(driver, 3).until(startButtonPresent)
    except TimeoutException:
        print("> Timed out while waiting for site to load.")
        driver.close()
        sys.exit(-1)
    startButton.click()
    myMouse = pynput.mouse.Controller()
    for i in range(limit):
        whiteSquaresPresent = EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".square.active"))
        try:
            whiteSquares = WebDriverWait(driver, 3).until(whiteSquaresPresent)
        except TimeoutException:
            print("> Timed out while waiting for white squares to appear.")
            driver.close()
            sys.exit(-1)
        time.sleep(1.5)
        # this sample will only contain blue squares
        allSquares = driver.find_elements_by_class_name("square")
        # look through current squares and see if any of them where white by comparing their coordinates
        indexWhiteSquares = 0
        for square in allSquares:
            if (indexWhiteSquares == len(whiteSquares)):
                break
            elif (square.rect["x"] == whiteSquares[indexWhiteSquares].rect["x"] and square.rect["y"] == whiteSquares[indexWhiteSquares].rect["y"]):
                square.click()
                indexWhiteSquares += 1
        time.sleep(1)


def handleVisualMemoryFast(limit):
    """Faster than handleVisualMemory but uses pynput to click,
    which means that it is less stable since the white squares can't be obstructed
    by any other window, the browser has to be maximized and the vertical offset
    for the coordinate might not work on different screen resolutions.
    More 'aggressive' since it grabs your mouse"""
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
            print("> Timed out while waiting for white squares to appear.")
            driver.close()
            sys.exit(-1)
        time.sleep(1.5)
        # iterate through all white squares and click on their location
        verticalOffset = 80
        for square in activeSquares:
            coordinates = (square.rect["x"] + (square.rect["width"] / 2),
                           square.rect["y"] + (square.rect["height"] / 2) + verticalOffset)
            myMouse.position = coordinates
            myMouse.click(pynput.mouse.Button.left, 1)
        time.sleep(1)


# the most challenging test of all
def handleHearing():
    time.sleep(0.25)
    driver.find_element_by_class_name("hero-button").click()
    driver.find_element_by_class_name("hero-button").click()
    print("> I can hear everything")


def handleTyping():
    time.sleep(0.5)
    textbox = driver.find_element_by_class_name("letters")
    myKeyboard = pynput.keyboard.Controller()
    myMouse = pynput.mouse.Controller()
    coordinates = (textbox.rect["x"] + (textbox.rect["width"] / 2),
                   textbox.rect["y"] + (textbox.rect["height"] / 2) + 80)
    textList = []
    # Each letter is a <div> element of class "incomplete"
    textElements = driver.find_elements_by_class_name("incomplete")
    print("> Starting to build string...")
    # join all letters to create a string to type
    # I have no idea why this takes so long
    for textElement in textElements:
        currentChar = textElement.text
        if (currentChar == ""):
            textList.append(" ")
        else:
            textList.append(currentChar)
        # a simple way of displaying the progress for this loop, since it can take many seconds
        print("> Completed %d / %d" %
              (len(textList), len(textElements)), end='\r')
        sys.stdout.flush()
    text = "".join(textList)
    # add a \n so the stdout flushes correctly for the next print()
    print("")
    print("> Typing...")
    # pynput's type() is more than 10 x faster than
    # textbox.send_keys(text)
    # but the textbox needs to be in focus for pynput, so click it
    myMouse.position = coordinates
    myMouse.click(pynput.mouse.Button.left, 1)
    myKeyboard.type(text)


if (len(sys.argv) >= 2 and (sys.argv[1] == "-help" or sys.argv[1] == "help")):
    printHelp(True)
    sys.exit(0)
else:
    # default limit, can be changed with launch option -limit
    limit = 10
    # wether the faster or stabler version of a test should be executed,
    # fast by default, can be set to stable by adding "stable" as last launch argument
    fast = True
    if (len(sys.argv) >= 4 and sys.argv[2] == "-limit"):
        if (sys.argv[3].isdigit()):
            limit = int(sys.argv[3])
        else:
            print("> Invalid -limit argument")
            sys.exit(-1)
    options = webdriver.ChromeOptions()
    # specify your Chrome browser location
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    options.add_argument("--start-maximized")
    # 'excludeSwitches' and 'enable-automation' disable the header "this browser is controlled by automated software"
    # this makes a difference for tests that rely on pixel coordinates, such as visual_memory
    # '--load-extension' disables the pop-up warning to disable extensions in developer mode, which can mess with
    # things such as 'send_keys()'
    options.add_experimental_option(
        "excludeSwitches", ['enable-automation', '--load-extension'])
    # specify your chromedriver path
    chrome_driver_binary = "C:\\Program Files (x86)\\Google\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(
        executable_path=chrome_driver_binary, options=options)
    if (len(sys.argv) > 1):
        print("> Starting test: " + sys.argv[1])
        # check if 'safe' parameter is set
        if ((len(sys.argv) >= 3 and sys.argv[2] == "stable") or (len(sys.argv) == 5 and sys.argv[4] == "stable")):
            fast = False
        handleUserInput(sys.argv[1], limit, fast)
    else:
        printHelp(False)
        handleUserInput(None, limit, fast)
