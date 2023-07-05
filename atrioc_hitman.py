# Imports
import time
import cv2
import mss
import numpy
import pytesseract
import re
import os
from tkinter import *
from tkinter.ttk import *
from threading import Timer
from screeninfo import get_monitors
import sv_ttk

# Adds Path to Tesseract (See Installation https://github.com/tesseract-ocr/tesseract#installing-tesseract)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Utility Functions

## Custom Threading Class 
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

## Removes all non-alphanumeric characters
def clean_text(string):
    return re.sub(r'\W+', '', string)

# Main Kill Loop
def kill_check():
    running_indicator.set("Script IS RUNNING!!")
    with mss.mss() as sct:

        ## Picks correct screen, and adjusts position of text based on monitor resolution
        i = options.index(monitor.get()) 
        mn = sct.monitors[i + 1]
        wid = int(screens[i].width)
        ratio = wid / 1920
        defaults = {'t':int(839 * ratio),'l':int(133 * ratio),'w':int(476 * ratio),'h':int(88 * ratio)}
        mon = {'top': mn["top"] + defaults["t"], 'left': mn["left"] + defaults['l'], 'width':  defaults['w'], 'height': defaults['h'], 'mon' : i + 1}

        im = numpy.asarray(sct.grab(mon))
        text = pytesseract.image_to_string(im)
        extracted_string = clean_text(text).lower() 

        if "campaignf" in extracted_string:
            os.system("taskkill.exe /IM hitman3.exe /F")
        
    window.after(500, kill_check)


# TKinter Init 
window = Tk()
window.title("HITMAN AUTO TERMINATOR")
window.iconbitmap("favicon.ico")
window.geometry("400x520")
sv_ttk.set_theme("dark")
        
l = Label(window, text = "HITMAN AUTO TERMINATOR")
l.config(font =("", 20))
l.pack(pady = (20,20))
    
l2 = Label(window, text = "This is a small utlity that will auto kill HITMAN as soon as it sees the 'Campaign Failed' text. Close this window to shut down the program.", wraplength=300, anchor="center")
l2.config(font =("", 12))
l2.pack(pady = (10,20))
# Sets Monitor Options


l21 = Label(window, text = "Select the monitor that you will have HITMAN on:")
l21.config(font =("", 12))
l21.pack(pady = (10,10))

# Sets Monitor Options
unsorted_screens = []
options = []

for m in get_monitors():
    unsorted_screens.append(m)

screens = sorted(unsorted_screens, key=lambda d: d.x) 

for screen in screens:
    options.append(clean_text(screen.name) + "  |  "+ str(screen.width) + " x "+  str(screen.height))
       
monitor = StringVar(window)
monitor.set(options[0]) # default value

for option in options:
        R1 = Radiobutton(window, text=option, variable=monitor, value=option)
        R1.pack( anchor = W )

button = Button(text="Start Auto-Kill", command=kill_check)
button.pack(pady = (10,10))


running_indicator = StringVar()
running_indicator.set("SCRIPT IS NOT RUNNING BOOMER!!")
l31 = Label(window, textvariable  = running_indicator)
l31.config(font =("", 30), wraplength=400, anchor="center")
l31.pack(pady = (10,10))



l3 = Label(window, text = "developed with ♥ by atricord")
l3.config(font =("", 12))
l3.pack(pady = (10,0))

# Starts Code

window.mainloop()

