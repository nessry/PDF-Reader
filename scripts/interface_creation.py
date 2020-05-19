# -*- coding: utf-8 -*-

from tkinter import *
import webbrowser

# The different font to be used
HUGE_FONT = ("Verdana", 14)
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Helvetica", 8)

root = Tk()

max_width = root.winfo_screenwidth() - 20
max_height = root.winfo_screenheight() - 135
max_size = (max_width, max_height)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

# function to move interface to the middle of the screen
def move_to_center(window):
    
    window.update_idletasks()

    content_w = window.winfo_width()
    content_h = window.winfo_height()

    decoration_size = (window.winfo_rootx() - window.winfo_x())
    outline_w = content_w + 2 * decoration_size
    outline_h = content_h + (window.winfo_rooty() - window.winfo_y())

    x = (window.winfo_screenwidth() - outline_w) // 2
    y = (window.winfo_screenheight() - outline_h) // 2
    window.geometry('+{}+{}'.format(x, y))
    
# create website link
def create_link(parent, url, width=None):
    
    msg = Message(parent, text=url)
    msg.config(font=NORM_FONT, foreground="blue", cursor='hand2')
    
    if width is not None:
        msg.config(width=w)
        
    msg.bind('<Button-1>', lambda event: webbrowser.open_new(url))
    
    return msg

# create tooltip for different buttons
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        
        self.tipwindow = tw = Toplevel(self.widget)
        
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        
        tw = self.tipwindow
        self.tipwindow = None
        
        if tw:
            tw.destroy()
            
def CreateToolTip(widget, text):
    
    toolTip = ToolTip(widget)
    
    def enter(event):
        toolTip.showtip(text)
        
    def leave(event):
        toolTip.hidetip()
        
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    


