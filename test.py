import tkinter as tk
from tkinter import ttk

class NBitNum(tk.IntVar):
    def __init__(self, value=10, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = value


    def get(self, base=10):
        if base == 10:
            return self.value
        elif base == 16:
            return f"{self.value:X}"



# create main window
main_window = tk.Tk()


print(f"{7:04b}")


# main loop
main_window.mainloop()


