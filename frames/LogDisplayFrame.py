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

        # tkinter widgets

        # scrollbar
        self.log_scroll_y = tk.Scrollbar(self)
        self.log_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_scroll_x = tk.Scrollbar(self, orient='horizontal')
        self.log_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # log text box
        self.log_text_box = tk.Text(self, yscrollcommand=self.log_scroll_y.set, wrap="none")
        self.log_text_box = tk.Text(self, xscrollcommand=self.log_scroll_x.set, wrap="none")
        self.log_text_box.pack(expand=True, fill=tk.BOTH)

        # configure scrollbar
        self.log_scroll_y.configure(command=self.log_text_box.yview)
        self.log_scroll_x.configure(command=self.log_text_box.xview)

        # display initial contents
        self.display_log()


    # LogDisplayFrame methods

    def display_log(self):
        # split text into lines
        # (newest log events at the top)
        log_lines = self.log_text.get().splitlines()
        self.log_text_box.delete(1.0, tk.END) # clear text box
        for log_entry in log_lines:
            self.log_text_box.insert(tk.END, log_entry + "\n")







