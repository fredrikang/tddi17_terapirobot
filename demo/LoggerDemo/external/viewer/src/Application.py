from tkinter import *
from Log import Log
from ChatBubble import ChatBubble
from ScreenMetrics import ScreenMetrics
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF

class Application(tk.Frame):
    def __init__(self, Log, master=None, ScreenMetrics='tk.Frame'):
        super().__init__(master)
        self.master = master    
        self.log = Log
        self.screenmetrics = ScreenMetrics
        self.bubbles = []
    
    def createChatBubbles(self, selected):
        for idx in range(1, len(self.log.data[selected])):
            user = self.log.getUser(selected, idx)
            if user != 'null':
                self.bubbles.append(ChatBubble(self.canvas, color="light grey", timestamp=self.log.getTimeStamp(selected, idx), message=self.log.getMessage(selected, idx, 56), user=user, screenmetrics=self.screenmetrics))
       
        if(not self.bubbles):
            self.bubbles.append(ChatBubble(self.canvas, color="light grey", timestamp="null", message="[EMPTY]", user="null", screenmetrics=self.screenmetrics))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def listBoxSelectedItemChanged(self, evt):
        """
        On listbox selected item changed, re-print all chatbubbles.
        """
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.bubbles.clear()
        
        w = evt.widget
        self.selected = w.get(int(w.curselection()[0]))
        self.createChatBubbles(self.selected)

    def loadLogList(self):
        for key in self.log.data:
            self.logList.insert(END, key)

    def createWidgets(self):
        self.logList = tk.Listbox(self.master)
        self.logList.grid(row=0, column=0, rowspan=16, sticky="ns")
        self.logList.bind('<<ListboxSelect>>', self.listBoxSelectedItemChanged)
        
        self.canvas = tk.Canvas(self.master, bg="white", width=self.screenmetrics.width*0.865, height=self.screenmetrics.height*0.95)
        self.canvas.grid(row=0, column=1, columnspan=4, rowspan=5)
        self.scroll = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scroll.grid(row=0, column=14, rowspan=16, sticky="ns")
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.createToolBar()
        self.loadLogList()
    
    def createToolBar(self):
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu = tk.Menu(self.menubar)
        self.exportMenu = tk.Menu(self.fileMenu)
        self.fileMenu.add_cascade(label="Export", menu=self.exportMenu)
        self.exportMenu.add_command(label="Export Text", command=self.exportLogToText)
        self.exportMenu.add_command(label="Export PDF", command=self.exportLogToPDF)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

    def exportLogToText(self):
        f = tk.filedialog.asksaveasfile(initialdir = "user.home", title="Export Log", filetypes=(("text files", "*.txt"),("all files", "*.*")))
        for idx in range(1, len(self.log.data[self.selected])):
            user = self.log.getUser(self.selected, idx)
            if user != 'null':
                f.write(user.upper()  + ' (' + self.log.getTimeStamp(self.selected, idx) + '):')
                f.write('\n' + self.log.getMessage(self.selected, idx, 128) + '\n\n\n')
        f.close()

    def exportLogToPDF(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_title(self.selected)
        f = tk.filedialog.asksaveasfile(initialdir = "user.home", mode="wb", title="Export Log", filetypes=(("pdf files", "*.pdf"),("all files", "*.*")))
        for idx in range(1, len(self.log.data[self.selected])):
            user = self.log.getUser(self.selected, idx)
            if user != 'null':
                text = user.upper()  + ' (' + self.log.getTimeStamp(self.selected, idx) + '):' 
                pdf.set_font("Arial", size=12, style='B')
                pdf.multi_cell(200, 5, txt=text)
                pdf.set_font("Arial", size=12, style='')
                text = self.log.getMessage(self.selected, idx, 128) + '\n\n\n'
                pdf.multi_cell(200, 5, txt = text)

        f.write(pdf.output(dest='S').encode('latin-1'))
        f.close()