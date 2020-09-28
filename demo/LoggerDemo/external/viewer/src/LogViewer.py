import json
import tkinter as tk
from application import Application
from Log import Log

log = Log()

root = tk.Tk(className = 'Log Viewer')
root.geometry("800x600")
app = Application(Log = log, master = root)
app.createWidgets()
app.mainloop()
