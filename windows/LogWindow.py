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
        self.always_on_top = tk.BooleanVar(value=False)


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

        keep_at_top_checkbox = ttk.Checkbutton(     self.log_window,
                                                    text="Keep window on top",
                                                    variable=self.always_on_top,
                                                    onvalue=True,
                                                    offvalue=False,
                                                    style="MCUTickbox3.TCheckbutton",
                                                    padding=5,
                                                    takefocus=False,
                                                    command=self._toggle_keep_on_top      )
        keep_at_top_checkbox.grid(column=0, row=1, pady=(0,0), padx=(0,0), sticky="EW")
        

    ## LogWindow methods

    def _toggle_keep_on_top(self):
        if self.always_on_top.get() == True:
            self.log_window.attributes('-topmost', True)
        else:
            self.log_window.attributes('-topmost', False)

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

