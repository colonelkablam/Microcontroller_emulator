import tkinter as tk
from tkinter import ttk
from my_constants import *


class LogDisplayFrame(ttk.Frame):
    def __init__(self, parent, log_text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # styling
        self.configure(style="Main.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid(sticky="NSEW")

        # object properties
        self.parent = parent
        self.log_text = log_text
        _code_text_size = 12

        # tkinter widgets

        # scrollbar
        log_scroll_y = ttk.Scrollbar(self)
        log_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        log_scroll_x = ttk.Scrollbar(self, orient='horizontal')
        log_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # log text box
        self.log_text_box = tk.Text(    self,
                                        yscrollcommand=log_scroll_y.set,
                                        xscrollcommand=log_scroll_x.set, 
                                        bg=LOG_BACKGROUND_LIGHT, 
                                        fg=LOG_BACKGROUND_DARK, 
                                        font=("Courier", _code_text_size), 
                                        wrap="none")
        self.log_text_box.pack(expand=True, fill=tk.BOTH)

        # configure scrollbar
        log_scroll_y.configure(command=self.log_text_box.yview)
        log_scroll_x.configure(command=self.log_text_box.xview)

        # display initial contents
        self.display_log()


    ## LogDisplayFrame methods

    def display_log(self):
        # split text into lines
        # (newest log events at the top)
        log_lines = self.log_text.get().splitlines()
        self.log_text_box.delete(1.0, tk.END) # clear text box
        for log_entry in log_lines:
            self.log_text_box.insert(tk.END, log_entry + "\n")

    def toggle_dark_theme(self, dark_display):
        if dark_display == True:
            self.log_text_box.configure(background=LOG_BACKGROUND_DARK, foreground=LOG_BACKGROUND_LIGHT)
        else:
            self.log_text_box.configure(background=LOG_BACKGROUND_LIGHT, foreground=LOG_BACKGROUND_DARK)








