import tkinter as tk

class ScreenMetrics:
    def __init__(self, tk):
        self.width = 1307#tk.winfo_screenwidth() * 0.95 * 0.4
        self.height = 800#tk.winfo_screenheight() * 0.85 * 0.7
        self.resolution = str(int(self.width))+'x'+str(int(self.height))
       #self.onResize = self.onResize.bind(self.resolution, self.width, self.height, tk)

"""
    def onResize(self, tk, height, width, resolution):
        width = tk.winfo_reqwidth() * 0.95
        height = tk.winfo_reqheight() * 0.85
        resolution = str(self.width)+'x'+str(self.height)
        """