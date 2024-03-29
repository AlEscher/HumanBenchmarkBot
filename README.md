# HumanBenchmarkBot

A python bot meant to ace the tests presented at [HumanBenchmark](https://www.humanbenchmark.com/)

## Requirements

### Python
I'm using Python 3.7.2 on Windows 10

Python libraries used for HumanBenchmarkBot.py:
* selenium
* pynput
* pywin32

Python libraries used for the single scripts:
* pytesseract
* pywin32
* pynput
* pillow

### Tesseract OCR
Most **single scripts** use [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) in order to recognize the text on the website. [Here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0-bibtag19.exe) is an installer for Windows.
If you use the BenchmarkBot, you will only need Chrome and a chromedriver

## How to use

### How to use the Bot (Recommended)
* Clone this repository or just download [HumanBenchmarkBot.py](HumanBenchmarkBot.py)
* `pip install` the needed libraries
* You will need a Chrome Browser and the according [chromedriver](https://sites.google.com/chromium.org/driver/) for your Browser version
* You may need to adjust [the path](HumanBenchmarkBot.py#L392-L395) to your chromedriver / chrome executable
* That's it start the Bot with `python HumanBenchmarkBot.py` for further instructions

### How to use a single script
* Clone this repository or download a single script you want to use
* Install Tesseract OCR and `pip install` the needed libraries
* Open [HumanBenchmark](https://www.humanbenchmark.com/) in your favourite browser and select one of the supported tests
* Be sure to have your browser in (windowed) Fullscreen mode and to be at the top of the page, aswell as having the display size of your browser and OS set to default 100%
* Run the according script (e.g. `python reaction_test.py`) from a shell (the shell-window shouldn't cover up the center of the test)
* Achieve perfection

## Previews

### Typing Test
![Typing Gif](Previews/typing.gif)
### Reaction Test
![Reaction Gif](Previews/reaction_test.gif)
### Verbal Memory Test
![Verbal Memory Gif](Previews/verbal_memory.gif)
### Visual Memory Test
![Visual Memory Gif](Previews/visual_memory.gif)
