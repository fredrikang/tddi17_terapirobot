import tkinter as tk

# Used for adjusting the screen resolution width and height.

class ScreenMetrics:
    """
    Represents the widget screen size.
    """
    def __init__(self, tk):
        self.width = 1307
        self.height = 800
        self.resolution = str(int(self.width))+'x'+str(int(self.height))