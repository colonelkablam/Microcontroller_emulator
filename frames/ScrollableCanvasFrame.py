import tkinter as tk
from tkinter import ttk

class ScrollableCanvasFrame(tk.Frame):
    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # canvas
        self.scroll_canvas = tk.Canvas(self, width=width, height=height)
        self.scroll_canvas.grid(column=0, row=0, sticky="NS")

        # scrollbars
        code_scroll = ttk.Scrollbar(self, orient='vertical', command=self.scroll_canvas.yview)
        code_scroll.grid(column=1, row=0, sticky="NS")

        # configure canvas
        self.scroll_canvas.configure(yscrollcommand=code_scroll.set)
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.scroll_canvas.bind('<Leave>', self._unbound_to_mousewheel)

        # create ANOTHER inner frame inside canvas
        self.inner_frame = ttk.Frame(self.scroll_canvas, style="MCUmemory.TFrame")

        # add INNER FRAME to a window in the canvas
        self.scroll_canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

    # get inner frame to mount elemets on
    def get_inner_frame(self):
        return self.inner_frame

    # canvas scrolling behaviour
    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bound_to_mousewheel(self, event):
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.scroll_canvas.unbind_all("<MouseWheel>")

