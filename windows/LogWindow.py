import tkinter as tk
from tkinter import ttk
from frames import LogDisplayFrame
from my_constants import *


class LogWindow:
    def __init__(self, parent):

        # LogWindow properties

        # starting position relative to parent window
        window_width = LOG_WINDOW_WIDTH
        window_height = LOG_WINDOW_HEIGHT
        window_xpos = parent.winfo_x()
        window_ypos = parent.winfo_y() + 100

        self.parent = parent


        # tkinter Widgets

        # create the new window to display log
        self.log_window = tk.Toplevel()
        self.log_window.title("Log Message Display")
        self.log_window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_xpos, window_ypos))
        # style
        self.log_window["background"] = COLOUR_MAIN_BACKGROUND
        self.log_window.rowconfigure(0, weight=1)
        self.log_window.columnconfigure(0, weight=1)
        self.log_window.configure(takefocus=True)
        # bind functions
        self.log_window.wm_protocol('WM_DELETE_WINDOW', self.on_close_window) # clean up after window close

        # create a LogDisplayFrame - put in new LogWindow; needs parent (MainWindow's log StringVar)
        self.log_frame = LogDisplayFrame(self.log_window, self.parent.log_text)
        self.log_frame.grid(column=0, row=0, sticky="NSEW")


        # LogWindow methods

    def update_window(self):
        self.log_frame.display_log()
    
    # clean up when closing window
    def on_close_window(self):
        # destroy the toplevel window
        self.log_window.destroy()
        # clear log_window var in MainWindow
        self.parent.close_log_window()

    def lift_window(self):
        self.log_window.lift()

