import tkinter as tk
import tkinter.font as font
from my_constants import *
from tkinter import ttk
from platform_specific import set_dpi_awareness, set_icon
from windows import MainWindow
from styling import MainStyle

# adjust for high def display - seems to cause resizing issues
# set_dpi_awareness()

# set window icon
icon = set_icon()

# create main window + add icon
main_window = MainWindow()
main_window.iconbitmap(True, icon)

# styling
font.nametofont("TkDefaultFont").configure(size=10)
style = MainStyle(main_window)

# main loop
main_window.mainloop()

