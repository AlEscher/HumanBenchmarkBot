try:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import selenium.common.exceptions as seleniumexcept
except ImportError:
    print("Missing selenium module")
    print("Please install it, e.g. 'pip install selenium'")
    exit(1)

try:
    import pynput
except ImportError:
    print("Missing pnyput module")
    print("Please intall it, e.g. 'pip install pnyput'")
    exit(1)

from ctypes import windll
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
        url = "https://www.humanbenchmark.com/"
        driver.get(url)

        if (userInput == "number_memory"):
            driver.get(url + "/tests/number-memory")
            handleNumberMemory(limit)
        elif(userInput == "reaction_time"):
            driver.get(url + "/tests/reactiontime")
            if (fast):
                handleReactionTimeFast()
            else:
                handleReactionTimeStable()
        elif (userInput == "verbal_memory"):
            driver.get(url + "/tests/verbal-memory")
            handleVerbalMemory(limit)
        elif (userInput == "visual_memory"):
            driver.get(url + "/tests/memory")
            handleVisualMemory(limit, fast)
        elif (userInput == "typing"):
            driver.get(url + "/tests/typing")
            handleTyping(fast)
        elif (userInput == "aim_trainer"):
            driver.get(url + "/tests/aim")
            handleAimTest()
        elif (userInput == "chimp"):
            driver.get(url + "/tests/chimp")
            handleChimpTest(limit)
        else:
            print("> Unknown test: " + userInput)
    handleUserInput(
        input("\n> What next? (Type help for help)\n# "), limit, fast)


def printHelp(isLaunchArgument):
    """Prints a help for this script, depending on the way "help" was called"""
    if (isLaunchArgument):
        print("> Usage example: python %s typing" % (sys.argv[0]))
        print("> Set an optional limit: %s verbal_memory -limit 100" %
              sys.argv[0])
        print(
            "> Start the stable version: %s visual_memory -limit 40 stable" % sys.argv[0])
        print("> To print this help: python %s -help" % sys.argv[0])
        print("> Available tests:\n\t- number_memory\n\t- reaction_time\n\t- verbal_memory\n\t- visual_memory\n\t- hearing\n\t- typing\n\t- aim_trainer\n\t- chimp")
    else:
        print("> Available commands:")
        print("\t- 'quit' : Terminates this program")
        print("\t- 'close' : Terminates this program and closes the browser")
        print("\t- 'help' : Prints this help")
        print("\t- '-limit x': Sets the limit to x")
        print("\t- 'fast' / 'stable' : Switch between fast and stable execution of the next tests")
        print("\t- 'testname' : Starts the test \"testname\"")
        print("> Available tests:\n\t- number_memory\n\t- reaction_time (fast / stable)\n\t- verbal_memory\n\t- visual_memory (fast / stable)\n\t- typing (fast / stable)\n\t- aim_trainer\n\t- chimp")


def handleNumberMemory(limit):
    wait = 3
    # get and click the start button
    startButton = driver.find_element_by_xpath("//button[text()='Start']")
    startButton.click()

    for i in range(limit):
        print("> Executing test: %d / %d" % (i + 1, limit), end='\r')
        sys.stdout.flush()
        # save the current number
        number = driver.find_element_by_class_name("big-number").text

        # wait for and get the input field, type in the number and press RETURN
        inputFieldPresent = EC.presence_of_element_located(
            # look for an input element with type "text" that only allows numbers
            (By.XPATH, "//input[@type='text' and @pattern='[0-9]*']"))
        try:
            # wait for the input field to become selectable,  with 'wait' as our max waiting time
            inputField = WebDriverWait(driver, wait).until(inputFieldPresent)
        except TimeoutException:
            print("> Timed out while waiting for input field.")
            sys.exit(-1)
        inputField.send_keys(number)
        inputField.send_keys(Keys.RETURN)
        nextButton = driver.find_element_by_xpath("//button[text()='NEXT']")
        nextButton.click()
        # the time the number is displayed for increases for each digit added
        wait += 1
    # clear stdout
    print("")


def handleReactionTimeFast():
    """This version is faster, but requires a specific pixel on your screen to be monitored constantly,
    which means your browser has to be maximised and you need to be scrolled to the top.
    This method grabs your mouse to click"""
    myMouse = pynput.mouse.Controller()
    dc = windll.user32.GetDC(0)
    gdi = windll.gdi32
    limit = 5
    # the center of the green / red window
    window = driver.find_element_by_xpath(
        "//div[@class='css-42wpoy e19owgy79']")
    x = window.rect["x"] + (window.rect["width"] // 2)
    y = window.rect["y"] + (window.rect["height"] // 2) + 160
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
                    "//div[@class='css-1qvtbrk e19owgy78']/h1/div")
                print("> Took", timeDisplay.text)
            except seleniumexcept.NoSuchElementException:
                print("> Couldn't find time display, maybe the absolute XPath changed?")
            # don't click next if this was the last run
            if (num < limit):
                myMouse.click(pynput.mouse.Button.left, 1)
            else:
                return


def handleReactionTimeStable():
    """More stable but not recommended, since it's slower than most humans..."""
    startScreenPresent = EC.presence_of_element_located(
        (By.XPATH, "//div[@class='css-42wpoy e19owgy79']"))
    try:
        WebDriverWait(driver, 3).until(startScreenPresent).click()
    except TimeoutException:
        print("> Timed out while waiting for the start screen...")
        sys.exit(-1)

    limit = 5
    for i in range(limit):
        greenPanelPresent = EC.presence_of_element_located(
            (By.XPATH, "//div[text()='Wait for green']"))
        # wait until screen becomes green
        try:
            WebDriverWait(driver, 15).until(greenPanelPresent).click()
        except TimeoutException:
            print("> Green panel took too long to appear...")
            return
        time.sleep(0.1)
        try:
            timeDisplay = driver.find_element_by_xpath("//div[@class='css-1qvtbrk e19owgy78']/h1/div")
            print("> Took", timeDisplay.text)
        except seleniumexcept.NoSuchElementException:
            print("> Couldn't find time display, maybe the absolute XPath changed?")
        # don't click next if this was the last run
        try:
            if (i != limit - 1):
                driver.find_element_by_xpath("//h2[text()='Click to keep going']").click()
            else:
                break
        except seleniumexcept.NoSuchElementException:
            print("> Couldn't continue with the test")


def handleVerbalMemory(limit):
    # get and click the start button
    # wait for the start button, as the site can take a second to load for this test
    startButtonPresent = EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Start']"))
    try:
        startButton = WebDriverWait(driver, 6).until(startButtonPresent)
    except TimeoutException:
        print("> Timed out while waiting for site to load.")
        sys.exit(-1)
    startButton.click()
    alreadySeen = []

    # keep collecting words and checking if we already saw them
    for i in range(limit):
        print("> Executing test: %d / %d" % (i + 1, limit), end='\r')
        sys.stdout.flush()
        currentWord = driver.find_element_by_class_name("word").text
        if (alreadySeen.count(currentWord) > 0):
            driver.find_element_by_xpath("//button[text()='SEEN']").click()
        else:
            alreadySeen.append(currentWord)
            driver.find_element_by_xpath("//button[text()='NEW']").click()
    # clear stdout
    print("")


def handleVisualMemory(limit, fast):
    """Faster than handleVisualMemory but uses pynput to click,
    which means that it is less stable since the white squares can't be obstructed
    by any other window, the browser has to be maximized and the vertical offset
    for the coordinate might not work on different screen resolutions.
    More 'aggressive' since it grabs your mouse"""
    startButtonPresent = EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Start']"))
    try:
        startButton = WebDriverWait(driver, 6).until(startButtonPresent)
    except TimeoutException:
        print("> Timed out while waiting for site to load.")
        sys.exit(-1)
    startButton.click()
    myMouse = pynput.mouse.Controller()
    for i in range(limit):
        print("> Executing test: %d / %d" % (i + 1, limit), end='\r')
        sys.stdout.flush()
        # wait for and save all whiteSquare WebElements
        whiteSquaresPresent = EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".square.active"))
        try:
            whiteSquares = WebDriverWait(driver, 3).until(whiteSquaresPresent)
        except TimeoutException:
            print("> Timed out while waiting for white squares to appear.")
            sys.exit(-1)
        time.sleep(1.5)
        # iterate through all white squares and click on their location
        if (fast):
            verticalOffset = 80
            for square in whiteSquares:
                coordinates = (square.rect["x"] + (square.rect["width"] / 2),
                               square.rect["y"] + (square.rect["height"] / 2) + verticalOffset)
                myMouse.position = coordinates
                myMouse.click(pynput.mouse.Button.left, 1)
        else:
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
    # clear stdout
    print("")


def handleTyping(fast):
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
        print("> Completed %d%%" %
              int((len(textList) / len(textElements)) * 100), end='\r')
        sys.stdout.flush()
    text = "".join(textList)
    # add a \n so the stdout flushes correctly for the next print()
    print("")
    print("> Typing...")
    # pynput's type() is more than 10 x faster than
    # textbox.send_keys(text)
    # but the textbox needs to be unobstracted by other windows
    if (fast):
        myMouse.position = coordinates
        myMouse.click(pynput.mouse.Button.left, 1)
        myKeyboard.type(text)
    else:
        textbox.send_keys(text)

    resultPresent = EC.presence_of_element_located(
        (By.XPATH, "//h1[@class='css-0']"))
    try:
        wpm = WebDriverWait(driver, 5).until(resultPresent).text
        # accuracy = driver.find_element_by_xpath("/html/body/div/div/div[4]/div[1]/div/div[1]/p").text
    except:
        print("> There was a problem getting the results")
        return
    print("> Finished with: %s" % (wpm))


def handleAimTest():
    targetPresent = EC.element_to_be_clickable(
        (By.XPATH, "//div[@data-aim-target='true']/div[@style='width: 100px; height: 2px;']"))
    try:
        target = WebDriverWait(driver, 6).until(targetPresent)
        target.click()
    except TimeoutException:
        print("> Timed out while waiting for site to load.")
        sys.exit(-1)

    for i in range(30):
        try:
            WebDriverWait(driver, 6).until(targetPresent).click()
        except:
            print("Failed to aim at target")


def handleChimpTest(limit):
    startButton = driver.find_element_by_xpath("//button[text()='Start Test']")
    startButton.click()


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
    options.add_argument("--start-maximized")
    # 'excludeSwitches' and 'enable-automation' disable the header "this browser is controlled by automated software"
    # this makes a difference for tests that rely on pixel coordinates, such as visual_memory
    # '--load-extension' disables the pop-up warning to disable extensions in developer mode, which can mess with
    # things such as 'send_keys()'
    options.add_experimental_option(
        "excludeSwitches", ['enable-automation', '--load-extension'])
    # specify your chromedriver path
    chrome_driver_binary = "C:\\Program Files\\Google\\chromedriver_win32\\chromedriver.exe"
    # specify your Chrome browser location
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    try:
        driver = webdriver.Chrome(executable_path=chrome_driver_binary, options=options)
    except seleniumexcept.WebDriverException:
        print("Failed to locate chrome.exe or the chromedriver")
        print("Please specify the correct path, as described in https://github.com/AlEscher/HumanBenchmarkBot#how-to-use-the-bot-recommended")
        exit(1)

    if (len(sys.argv) > 1):
        print("> Starting test: " + sys.argv[1])
        # check if 'safe' parameter is set
        if ((len(sys.argv) >= 3 and sys.argv[2] == "stable") or (len(sys.argv) == 5 and sys.argv[4] == "stable")):
            fast = False
        handleUserInput(sys.argv[1], limit, fast)
    else:
        printHelp(False)
        handleUserInput(None, limit, fast)
