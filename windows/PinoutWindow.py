import tkinter as tk
from tkinter import ttk
from my_constants import *


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
        self.pinout_window = tk.Toplevel()
        self.pinout_window.title("MCU Pinout")
        self.pinout_window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_xpos, window_ypos))
        # style
        self.pinout_window["background"] = COLOUR_MAIN_BACKGROUND
        self.pinout_window.rowconfigure(0, weight=1)
        self.pinout_window.columnconfigure(0, weight=1)
        # bind functions
        self.pinout_window.wm_protocol('WM_DELETE_WINDOW', self.on_close_window) # clean up after window close

        # create a PinoutDisplayFrame
        self.pinout_frame = ttk.Frame(self.pinout_window)
        self.pinout_frame.grid(column=0, row=0, sticky="NSEW")


        # PinoutWindow methods

    def update_window(self):
        pass
    
    # clean up when closing window
    def on_close_window(self):
        # destroy the toplevel window
        self.pinout_window.destroy()
        # clear pinout_window var in MainWindow
        self.parent.close_pinout_window()

    def lift_window(self):
        self.pinout_window.lift()


