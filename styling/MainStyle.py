import tkinter as tk
from tkinter import ttk
from my_constants import *

# styles in ttk.Style object for the ttk objects to use - CONSTANTS in my_constants module in root 

class MainStyle(ttk.Style):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Style properties
        self.theme_use("clam")

        # MainWindow styles
        self.configure(
            "MainWindowOuter.TFrame",
            background=COLOUR_MAIN_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )
        self.configure(
            "MainWindowInner.TFrame",
            background=COLOUR_INNER_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )

        self.configure(
            "MainWindowInner2.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )

        self.configure(
            "MainWindowOuter.TLabel", 
            background=COLOUR_MAIN_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 18, 'bold')
        )

        self.configure(
            "MainWindowOuterSlider.TLabel", 
            background=COLOUR_MAIN_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 10, 'bold')
        )

        self.configure(
            "MainWindowInner.TLabel", 
            background=COLOUR_INNER_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 14, 'bold')
        )

        self.configure(
            "MainWindowInner2.TLabel", 
            background=COLOUR_INNER_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 9)
        )

        
        self.configure(
            "MainWindowInner3.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 9)
        )

        self.configure(
            "MainWindow.TButton",
            background=COLOUR_BUTTON_NORMAL,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)
        )
        self.configure(
            "MainWindow2.TButton",
            background=COLOUR_BUTTON_NORMAL_2,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)
        )

        self.configure(
            "MainWindow3.TButton",
            background=COLOUR_BUTTON_NORMAL_3,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)
        )
        self.configure(
            "MainWindow4.TButton",
            background=COLOUR_BUTTON_NORMAL_4,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)
        )

        self.map(
            "MainWindow.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        self.map(
            "MainWindow2.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        self.map(
            "MainWindow3.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        # MCUFrame Styles
        self.configure(
            "MCUmemory.TLabel", 
            background=COLOUR_MEMORY_LABEL_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 9)
        )

        self.configure(
            "MCUTickbox.TCheckbutton", 
            background=COLOUR_MEMORY_FRAME_BACKGROUND,
            indicatorforeground =DATA_MEMORY_HIGHLIGHT,
        )

        self.configure(
            "MCUmemory.TFrame",
            background=COLOUR_MEMORY_FRAME_BACKGROUND,
        )

        self.configure(
            "ByteDisplayHeading.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12, "bold")
        )

        self.configure(
            "MCUBitHighlight.TFrame",
            background=BIT_HIGHLIGHT,
            borderwidth=2,
            relief="ridge"
        )

        self.configure(
            "MCUByte.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )

        self.configure(
            "BitPosition.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 8)
        )

        self.configure(
            "MCUBit.TLabel", 
            background=COLOUR_MEMORY_LABEL_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 11)
        )

        self.configure(
            "MCUBitHighlight.TLabel", 
            background=BIT_HIGHLIGHT,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 11)
        )

        self.configure(
            "MCUByteValues.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
        )

        self.configure(
            "Stack.TLabel", 
            background=COLOUR_MEMORY_LABEL_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            relief="sunken",
            borderwidth=3,
            font=("Courier", 9)
        )

        self.configure(
            "StackHighlighted.TLabel", 
            background=STACK_HIGHLIGHT,
            foreground=COLOUR_DARK_TEXT,
            relief="sunken",
            borderwidth=3,
            font=("Courier", 9)
        )


        # CodeWindow Styles

        self.configure(
            "CodeWindow.TFrame",
            background=COLOUR_MAIN_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )

        self.configure(
            "CodeWindow.TLabel", 
            background=COLOUR_LIGHT_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 10)
        )

        self.configure(
            "CodeWindow.TButton",
            background=COLOUR_BUTTON_NORMAL,
            foreground=COLOUR_DARK_TEXT
        )

        self.map(
            "CodeWindow.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        self.configure(
            "CodeWindow2.TButton",
            background=COLOUR_BUTTON_NORMAL_2,
            foreground=COLOUR_DARK_TEXT
        )

        self.map(
            "CodeWindow2.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED_2), ("active", COLOUR_BUTTON_ACTIVE_2), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )