# HumanBenchmarkBot

A bot meant to ace the tests presented at [HumanBenchmark](https://www.humanbenchmark.com/)

## Requirements

### Tesseract OCR
Most scripts use [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) in order to recognize the text on the website. [Here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0-bibtag19.exe) is an installer for Windows

### Python libraries

Python libraries used:
* pytesseract
* pywin32api
* pynput
* pillow

## How to use

* Open [HumanBenchmark](https://www.humanbenchmark.com/) in your favourite browser and select one of the supported tests
* Be sure to have your browser in (windowed) Fullscreen mode and to be at the top of the page, aswell as having the display size of your browser and OS set to default 100%
* Run the according script (e.g. 'python reaction_test.py') from a shell (the shell-window shouldn't cover up the center of the test)
* Achieve perfection