import json
import tkinter as tk
from Application import Application
from Log import Log
from ScreenMetrics import ScreenMetrics

log = Log()

root = tk.Tk(className = 'Log Viewer')
screenmetrics = ScreenMetrics(root)
root.geometry(screenmetrics.resolution)

root.resizable(0,0) # This disables resize-able window.

app = Application(Log = log, master = root, ScreenMetrics = screenmetrics)
app.create_widgets()
app.mainloop()