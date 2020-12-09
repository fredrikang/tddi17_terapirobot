import json
import tkinter as tk
# -----------------------------------------------------------
# Class handling speech bubbles used in the UI.
#
# Used to encapsulate the log text to separate different utternaces.
# -----------------------------------------------------------
class ChatBubble:
    """
    Represents a speech bubble (rectangle) of a logs text object.
    Used for representing the conversation had in the selected log.
    """
    def __init__(self, master, color, timestamp, message, user, screenmetrics):
        self.master = master
        self.user = user
        self.frame = tk.Frame(master, bg=color)
        self.bgColor = "light grey"

        if self.user == 'user':
             self.i = self.master.create_window(screenmetrics.width*0.775, screenmetrics.height*0.95, window=self.frame)
             self.bgColor = "light green"
             self.frame.configure(background=self.bgColor)
        else:
             self.i = self.master.create_window(screenmetrics.width*0.125, screenmetrics.height*0.95, window=self.frame)
                
        tk.Label(self.frame, text=timestamp, bg=self.bgColor).grid(row=0, column=0, sticky="we", padx=5)
        tk.Label(self.frame, text=message, bg=self.bgColor).grid(row=1, column=0, sticky="we", padx=5, pady=3)
        self.master.master.update_idletasks()
        
        
        compensate_y = len(message.split('\n')) - 1
        self.master.move(tk.ALL, 0, -65)
        # Compensate for y in text with newlines (bigger bubble). Compensate based on the number of newlines present in the text.
        self.master.move(tk.ALL, 0, -15 * compensate_y)

    def draw_triangle(self, widget):
        """
        Unused.
        Will draw a "speech arrow" from the chat bubble.
        """
        x1, y1, x2, y2 = self.master.bbox(widget)
        if self.user == 'robot':
            return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2
        else:
            return x2, y2 - 10, x2 + 15, y2 + 10, x2, y2
