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
            background=[("pressed", COLOUR_BUTTON_PRESSED_2), ("active", COLOUR_BUTTON_ACTIVE_2), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        self.map(
            "MainWindow3.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED_3), ("active", COLOUR_BUTTON_ACTIVE_3), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        self.map(
            "MainWindow4.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED_4), ("active", COLOUR_BUTTON_ACTIVE_4), ("disabled", COLOUR_LIGHT_BACKGROUND)]
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
            indicatorforeground=CHECKBOX_TICK,
            font=("Courier", 9)
        )
        self.configure(
            "MCUTickbox2.TCheckbutton", 
            background=COLOUR_INNER_BACKGROUND,
            indicatorforeground=CHECKBOX_TICK,
            font=("Courier", 9)
        )

        self.configure(
            "MCUTickbox3.TCheckbutton", 
            background=COLOUR_INNER2_BACKGROUND,
            indicatorforeground=CHECKBOX_TICK,
            font=("Courier", 9)
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

        self.configure(
            "Instruction.TLabel", 
            background=COLOUR_MEMORY_LABEL_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)
        )

        self.configure(
            "StatusHeading.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 10, "bold")
        )


        # CodeWindow Styles

        self.configure(
            "CodeWindow.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
        )

        self.configure(
            "CodeWindowInner.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
            relief="ridge"
        )

        self.configure(
            "CodeWindow.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 10)
        )


        self.configure(
            "CodeWindow.TButton",
            background=COLOUR_BUTTON_NORMAL,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)

        )

        self.map(
            "CodeWindow.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        self.configure(
            "CodeWindow2.TButton",
            background=COLOUR_BUTTON_NORMAL_2,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 12)

        )

        self.map(
            "CodeWindow2.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED_2), ("active", COLOUR_BUTTON_ACTIVE_2), ("disabled", COLOUR_LIGHT_BACKGROUND)]
        )

        # pinout styles

        self.configure(
            "PinOutChip.TFrame",
            background=COLOUR_MAIN_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )
        
        self.configure(
            "PinOutChip.TLabel", 
            background=COLOUR_MAIN_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 11, 'bold')
        )

        self.configure(
            "PinOutHeading.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 8)
        )

        self.configure(
            "Pin.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
            borderwidth=2,
           # relief="ridge"
        )
        self.configure(
            "PinOutBackground.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
            borderwidth=2,
            relief="ridge"
        )

        self.configure(
            "PinOutBackground2.TFrame",
            background=COLOUR_INNER2_BACKGROUND,
        )

        self.configure(
            "PinOut.TLabel", 
            background=COLOUR_INNER2_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font=("Courier", 11)
        )

        self.configure(
            "PinOutON.TButton",
            background = COLOUR_PINOUT_BUTTON_ON,
            font=("Courier", 11)
        )

        self.map(
            "PinOutON.TButton",
            background=[("pressed", COLOUR_PINOUT_BUTTON_PRESSED), ("active", COLOUR_PINOUT_BUTTON_ACTIVE), ("disabled", COLOUR_INNER2_BACKGROUND)]
        )

        self.configure(
            "PinOutOFF.TButton",
            background = COLOUR_PINOUT_BUTTON_OFF,
            font=("Courier", 11)
        )

        self.map(
            "PinOutOFF.TButton",
            background=[("pressed", COLOUR_PINOUT_BUTTON_PRESSED), ("active", COLOUR_PINOUT_BUTTON_ACTIVE), ("disabled", COLOUR_INNER2_BACKGROUND)]
        )