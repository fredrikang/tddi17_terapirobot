import json
import tkinter as tk
from Application import Application
from Log import Log
from ScreenMetrics import ScreenMetrics

log = Log()

root = tk.Tk(className = 'Log Viewer')
screenmetrics = ScreenMetrics(root)
root.geometry(screenmetrics.resolution)

# This row makes it impossible to resize window.
root.resizable(0,0)

app = Application(Log = log, master = root, ScreenMetrics = screenmetrics)
app.createWidgets()
app.mainloop()