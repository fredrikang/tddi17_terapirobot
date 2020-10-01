from tkinter import *
from Log import Log

import tkinter as tk
class Application(tk.Frame):
    def __init__(self, Log, master=None):
        super().__init__(master)
        self.master = master    
        #self.pack()
        self.log = Log

    def loadLogList(self):
        for key in self.log.data:
            self.logList.insert(END, key)

    def createWidgets(self):
        self.logList = tk.Listbox(self.master, width=20)
        self.logList.grid(row=1, column=1, rowspan = 2)
        #self.logList.pack()
        self.loadLogList()
        
