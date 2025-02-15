from tkinter import *
from Log import Log
from ChatBubble import ChatBubble
from ScreenMetrics import ScreenMetrics
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF

# -----------------------------------------------------------
# Class handling all the UI components.
# -----------------------------------------------------------
class Application(tk.Frame):
    """
    The application that handles all UI.
    """
    def __init__(self, Log, master=None, ScreenMetrics='tk.Frame'):
        super().__init__(master)
        self.master = master    
        self.log = Log
        self.screenmetrics = ScreenMetrics
        self.bubbles = []
    
    def create_chat_bubbles(self, selected):
        """
        Create all chat bubbles (log text) from the selected log.
        """
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.bubbles.clear()
        
        max_iterations = 4 # Error handling caused by error prone read of data.
        idx = 1

        while idx < len(self.log.data[selected]) and max_iterations > 0:
            try:
                user = self.log.get_user(selected, idx)
                if user != 'null':
                    self.bubbles.append(ChatBubble(self.canvas, color="light grey", timestamp=self.log.get_timestamp(selected, idx), message=self.log.get_message(selected, idx, 56), user=user, screenmetrics=self.screenmetrics))
                idx = idx + 1
            except: 
                continue
            if idx is len(self.log.data[selected]):
                max_iterations = max_iterations - 1

        if(not self.bubbles):
            self.bubbles.append(ChatBubble(self.canvas, color="light grey", timestamp="null", message="[EMPTY]", user="null", screenmetrics=self.screenmetrics))

    def listbox_selected_item_changed(self, evt):
        """
        On listbox selected item changed, re-print all chatbubbles.
        """
        
        w = evt.widget
        try:
            self.selected = w.get(int(w.curselection()[0]))
            self.create_chat_bubbles(self.selected)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except:
            self.selected = ''

    def load_log_list(self):
        """
        Load the list of logs from the log object
        """
        for key in self.log.data:
            self.logList.insert(END, key)

    def create_widgets(self):
        """
        Create all widgets
        """
        self.logList = tk.Listbox(self.master)
        self.logList.grid(row=0, column=0, rowspan=16, sticky="ns")
        self.logList.bind('<<ListboxSelect>>', self.listbox_selected_item_changed)
        
        self.canvas = tk.Canvas(self.master, bg="white", width=self.screenmetrics.width*0.865, height=self.screenmetrics.height*0.95)
        self.canvas.grid(row=0, column=1, columnspan=4, rowspan=5)
        self.scroll = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scroll.grid(row=0, column=14, rowspan=16, sticky="ns")
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.create_toolbar()
        self.load_log_list()
    
    def create_toolbar(self):
        """
        Create toolbar for UI
        """
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu = tk.Menu(self.menubar)
        self.exportMenu = tk.Menu(self.fileMenu)
        self.fileMenu.add_cascade(label="Export", menu=self.exportMenu)
        self.exportMenu.add_command(label="Export Text", command=self.export_log_to_text)
        self.exportMenu.add_command(label="Export PDF", command=self.export_log_to_pdf)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

    def export_log_to_text(self):
        """
        Export the selected log to a .txt file
        Formatted as: 
            SPEAKER (timestamp):
            MESSAGE

            SPEAKER (timestamp):
             .
             .
             .

        Where SPEAKER is either user or robot and timestamp is the time of the dialog.
        """
        f = tk.filedialog.asksaveasfile(initialdir = "user.home", title="Export Log", filetypes=(("text files", "*.txt"),("all files", "*.*")))
        for idx in range(1, len(self.log.data[self.selected])):
            user = self.log.get_user(self.selected, idx)
            if user != 'null':
                f.write(user.upper()  + ' (' + self.log.get_timestamp(self.selected, idx) + '):')
                f.write('\n' + self.log.get_message(self.selected, idx, 128) + '\n\n\n')
        f.close()

    def export_log_to_pdf(self):
        """
        Export the selected log to a .pdf file (same formatting as in the .txt file)
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_title(self.selected)
        f = tk.filedialog.asksaveasfile(initialdir = "user.home", mode="wb", title="Export Log", defaultextension="*.*", filetypes=(("pdf files", "*.pdf"),("all files", "*.*")))
        for idx in range(1, len(self.log.data[self.selected])):
            user = self.log.get_user(self.selected, idx)
            if user != 'null':
                text = user.upper()  + ' (' + self.log.get_timestamp(self.selected, idx) + '):' 
                pdf.set_font("Arial", size=12, style='B')
                pdf.multi_cell(200, 5, txt=text)
                pdf.set_font("Arial", size=12, style='')
                text = self.log.get_message(self.selected, idx, 128) + '\n\n\n'
                pdf.multi_cell(200, 5, txt = text)

        f.write(pdf.output(dest='S').encode('latin-1'))
        f.close()