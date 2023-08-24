import tkinter as tk
from tkinter import ttk
from my_constants import *
from frames import ChipPinoutFrame



class PinoutWindow:
    def __init__(self, parent):

        # LogWindow properties

        # starting position relative to parent window
        window_width = PINOUT_WINDOW_WIDTH
        window_height = PINOUT_WINDOW_HEIGHT

        window_xpos = parent.winfo_x() + 500
        window_ypos = parent.winfo_y() + 50

        self.parent = parent

        self.always_on_top = tk.BooleanVar(value=False)

        # tkinter Widgets

        # create the new window to display pinout
        self.window = tk.Toplevel()
        self.window.title("MCU Pinout")
        #self.window.geometry("%dx%d+%d+%d" % (window_width, window_height, window_xpos, window_ypos))
        self.window.resizable(height = False, width = False)
        # style
        self.window["background"] = COLOUR_MAIN_BACKGROUND
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        # bind functions
        self.window.wm_protocol('WM_DELETE_WINDOW', self.hide) # clean up after window close

        ##  ChipPinoutFrame for display is created in MCU_frame ##

        # checkbox to keep window at the top
        keep_at_top_checkbox = ttk.Checkbutton(    self.window,
                                                        text="Keep window on top",
                                                        variable=self.always_on_top,
                                                        onvalue=True,
                                                        offvalue=False,
                                                        style="MCUTickbox3.TCheckbutton",
                                                        padding=5,
                                                        takefocus=False,
                                                        command=self._toggle_keep_on_top      )
        keep_at_top_checkbox.grid(column=0, row=1, pady=(0,0), padx=(0,0), sticky="EW")
        
        
    ## PinoutWindow methods

    def _toggle_keep_on_top(self):
        if self.always_on_top.get() == True:
            self.window.attributes('-topmost', True)
        else:
            self.window.attributes('-topmost', False)

    def lift_window(self):
        self.window.lift()

    def hide(self):
        self.window.withdraw()

    def show(self):
        self.window.deiconify()

