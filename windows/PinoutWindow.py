import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames import PinoutFrame



class PinoutWindow:
    def __init__(self, parent):

        # LogWindow properties

        # starting position relative to parent window
        window_width = PINOUT_WINDOW_WIDTH
        window_height = PINOUT_WINDOW_HEIGHT

        window_xpos = parent.winfo_x() + 500
        window_ypos = parent.winfo_y() + 50

        self.parent = parent

        # tkinter Widgets

        # create the new window to display pinout
        self.window = tk.Toplevel()
        self.window.title("MCU Pinout")
        self.window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_xpos, window_ypos))
        # style
        self.window["background"] = COLOUR_MAIN_BACKGROUND
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        # bind functions
        self.window.wm_protocol('WM_DELETE_WINDOW', self.hide) # clean up after window close

        ##  PinoutFrame for display is created in MCU_frame ##

        # PinoutWindow methods

    def lift_window(self):
        self.window.lift()

    def hide(self):
        self.window.withdraw()

    def show(self):
        self.window.deiconify()

