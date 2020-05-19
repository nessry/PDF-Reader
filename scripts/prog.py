# -*- coding: utf-8 -*-

import platform
import os
import shutil
from pathlib import Path
from tkinter.ttk import Frame, Button, Style
from tkinter import *
from PIL import Image, ImageTk
from interface_creation import  move_to_center, create_link, CreateToolTip, HUGE_FONT, LARGE_FONT, NORM_FONT, SMALL_FONT, root, max_width, max_height, max_size, w, h
from show_pdf import display_pdf
import pdf as pdf
import PySimpleGUI as sg
from datetime import datetime

#import images
images_dir = Path(__file__).absolute().parents[1] / 'images'
image = str(images_dir / 'welcome.png')
image_reg = str(images_dir / 'register.PNG')
image_log = str(images_dir / 'login.PNG')

if platform.system() == 'Windows':
    icon = r'{}\{}'.format(images_dir, 'logo.ico')
elif platform.system() == 'Linux':
    icon = '@{}/{}'.format(images_dir, 'logo.xbm')
else:
    raise RuntimeError('Unsupported OS {}.'.format(platform.system()))

gap_small = 2
gap = 6
gap_large = 18


# define welcome interface
class AccountWindow(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Welcome")
        self.iconbitmap(icon)
        self.resizable(0, 0)
        self.style = Style()
        self.style.theme_use("default")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        load = Image.open(image)

        # it might be better to resize image in file instead of adjusting size here
        if load.width > max_width / 2:
            ratio = (max_width / 2) / load.width
            load = load.resize(
                (int(ratio * load.width), int(ratio * load.height)),
                # Image.BICUBIC
            )

        render = ImageTk.PhotoImage(load)
        self._render = render  # to protect from garbage collector

        canvas = Canvas(self, width=load.width, height=load.height)
        canvas.create_image(0, 0, anchor=NW, image=render)
        canvas.grid(pady=(0, gap_large))

        w = load.width - 2 * gap_large

        text = (
            "You already have an account ?"
        )

        msg = Message(self, text=text, justify='left')
        msg.config(font=LARGE_FONT, width=w)
        msg.grid()

        self._login_button = Button(self, text='Login', default='active', bg="#020769", fg="white", font=HUGE_FONT)
        self._login_button.grid(sticky=W + E, padx=gap_large, pady=gap_large)
        CreateToolTip(self._login_button, text = 'Click this button to login\n'
                 'if you already have an\n'
                 'account in the system')
        msg = Message(self, text='___OR___', justify='left')
        msg.config(font=LARGE_FONT, width=w)
        msg.grid()
        
        self._register_button = Button(self, text='Register', default='active', bg="#020769", fg="white", font=HUGE_FONT)
        self._register_button.grid(sticky=W + E, padx=gap_large, pady=gap_large)
        CreateToolTip(self._register_button, text = 'Click this button to create\n'
                 'an account.')

        footer_frame = Frame(self)
        footer_frame.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(1, weight=1)
        footer_frame.grid(sticky=E + W)

        text = "All rights reserved"
        msg = Message(footer_frame, text=text)
        msg.config(font=NORM_FONT, width=w)
        msg.grid(row=0, column=0, sticky=W)

        link = create_link(footer_frame, "https://www.example.com", w)
        link.grid(row=0, column=1, sticky=E)

        move_to_center(self)

# define login interface
class LoginWindow(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        
        global username_verify
        global password_verify
        
        self.title("Login")
        self.iconbitmap(icon)
        self.resizable(0, 0)
        self.style = Style()
        self.style.theme_use("default")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        load = Image.open(image_log)

        # it might be better to resize image in file instead of adjusting size here
        if load.width > max_width / 2:
            ratio = (max_width / 2) / load.width
            load = load.resize(
                (int(ratio * load.width), int(ratio * load.height)),
                # Image.BICUBIC
            )

        render = ImageTk.PhotoImage(load)
        self._render = render  # to protect from garbage collector

        canvas = Canvas(self, width=load.width, height=load.height)
        canvas.create_image(0, 0, anchor=NW, image=render)
        canvas.grid(pady=(0, gap_large))

        w = load.width - 2 * gap_large
 
        username_verify = StringVar()
        password_verify = StringVar()

        text = (
            "Please enter your username and your password"
        )

        msg = Message(self, text=text, justify='left')
        msg.config(font=LARGE_FONT, width=w)
        msg.grid()
        
        entries_frame = Frame(self)
        entries_frame.columnconfigure(0, weight=1)
        entries_frame.columnconfigure(1, weight=1)
        entries_frame.grid(sticky=E + W)
        
        username_login_label = Label(entries_frame ,text = "Username * :",fg="#020769", font='bold').grid(row=0, column=0)
        username_login_entry = ttk.Entry(entries_frame, textvariable= username_verify, width=70).grid(row=0, column=1)
        
        password_login_lable = Label(entries_frame ,text = "Password * :",fg="#020769", font='bold').grid(row=1, column=0)
        password_login_entry = ttk.Entry(entries_frame, textvariable=password_verify, show='*', width=70).grid(row=1, column=1)
        
        self._login_button = Button(self, text='Login', default='active', bg="#020769", fg="white", font=HUGE_FONT)
        self._login_button.grid(sticky=W + E, padx=gap_large, pady=gap_large)
        CreateToolTip(self._login_button, text = 'Click this button to login\n'
                 'to your account.')
        
        self._cancel_button = Button(self, text='Cancel', default='active', bg="#787575", fg="white", font=HUGE_FONT)
        self._cancel_button.grid(sticky=W + E, padx=gap_large, pady=gap_large)
        CreateToolTip(self._cancel_button, text = 'Back <===')

        footer_frame = Frame(self)
        footer_frame.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(1, weight=1)
        footer_frame.grid(sticky=E + W)

        text = "All rights reserved"
        msg = Message(footer_frame, text=text)
        msg.config(font=NORM_FONT, width=w)
        msg.grid(row=0, column=0, sticky=W)

        link = create_link(footer_frame, "https://www.example.com", w)
        link.grid(row=0, column=1, sticky=E)

        move_to_center(self)

# define register interface
class RegisterWindow(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        
        # set global variables
        global username
        global password
        global _username_entry
        global _password_entry
        
        self.title("Register")
        self.iconbitmap(icon)
        self.resizable(0, 0)
        self.style = Style()
        self.style.theme_use("default")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        load = Image.open(image_reg)

        # it might be better to resize image in file instead of adjusting size here
        if load.width > max_width / 2:
            ratio = (max_width / 2) / load.width
            load = load.resize(
                (int(ratio * load.width), int(ratio * load.height)),
                # Image.BICUBIC
            )

        render = ImageTk.PhotoImage(load)
        self._render = render  # to protect from garbage collector

        canvas = Canvas(self, width=load.width, height=load.height)
        canvas.create_image(0, 0, anchor=NW, image=render)
        canvas.grid(pady=(0, gap_large))

        w = load.width - 2 * gap_large
        
        # Set text variables
        username = StringVar()
        password = StringVar()

        text = (
            "Please choose a username and a password"
        )

        msg = Message(self, text=text, justify='left')
        msg.config(font=LARGE_FONT, width=w)
        msg.grid()
        
        self.entries_frame = Frame(self)
        self.entries_frame.columnconfigure(0, weight=1)
        self.entries_frame.columnconfigure(1, weight=1)
        self.entries_frame.grid(sticky=E + W)
        
        username_label = Label(self.entries_frame ,text = "Username * :",fg="#020769", font='bold').grid(row=0, column=0)
        self._username_entry = ttk.Entry(self.entries_frame, textvariable=username, width=70).grid(row=0, column=1)
        
        password_lable = Label(self.entries_frame ,text = "Password * :",fg="#020769", font='bold').grid(row=1, column=0)
        self._password_entry = ttk.Entry(self.entries_frame, textvariable=password, show='*', width=70).grid(row=1, column=1)
        
        self._register_button = Button(self, text='Register', default='active', bg="#020769", fg="white", font=HUGE_FONT)
        self._register_button.grid(sticky=W + E, padx=gap_large, pady=gap_large)
        
        self._cancel_button = Button(self, text='Cancel', default='active', bg="#787575", fg="white", font=HUGE_FONT)
        self._cancel_button.grid(sticky=W + E, padx=gap_large, pady=gap_large)
        CreateToolTip(self._cancel_button, text = 'Back <===')
        
        footer_frame = Frame(self)
        footer_frame.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(1, weight=1)
        footer_frame.grid(sticky=E + W)

        text = "All rights reserved"
        msg = Message(footer_frame, text=text)
        msg.config(font=NORM_FONT, width=w)
        msg.grid(row=0, column=0, sticky=W)

        link = create_link(footer_frame, "https://www.example.com", w)
        link.grid(row=0, column=1, sticky=E)

        move_to_center(self)

# define main interface
class AdminWindow(Toplevel):

    def __init__(self, parent, width, height, x, y):
        super().__init__(parent)

        self.width = width

        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.title("Admin")
        self.iconbitmap(icon)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        toolbar_frame = Frame(self)
        toolbar_frame.rowconfigure(0, weight=1)
        toolbar_frame.columnconfigure(0, weight=1, uniform='buttons')
        toolbar_frame.columnconfigure(1, weight=1, uniform='buttons')
        
        toolbar_frame.grid(sticky=W + E)
        
        self._file_button = Button(toolbar_frame, text='FILE', bg="#020769", fg="white", font=LARGE_FONT)
        self._file_button.grid(row=0, column=0, sticky=E + W, padx=(gap_small, gap), pady=gap)
        CreateToolTip(self._file_button, text = 'Click this button to choose\n'
                 'a file.')
        
        self._logout_button = Button(toolbar_frame, text='LOGOUT', bg="#020769", fg="white", font=LARGE_FONT)
        self._logout_button.grid(row=0, column=1, sticky=E + W, padx=(gap_small, gap), pady=gap)
        CreateToolTip(self._logout_button, text = 'Click this button to logout\n'
                 'from your account.')
        
        self.canvas = Canvas(self, borderwidth=0, background="white")   
        self.main_frame = Frame(self.canvas, background="white", width=self.canvas.winfo_width(),height=self.canvas.winfo_height())
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set) 
        self.vsb.grid(row=1,column=1, sticky=NS)   
        self.hsb.grid(row=2,sticky=EW)                               #pack scrollbar to right of self
        self.canvas.grid(row=1,column=0,sticky=E + W + N + S)        #pack canvas to left of self and expand to fil
        self.main_frame.rowconfigure(0, weight=1, uniform='row')
        self.main_frame.rowconfigure(1, weight=1, uniform='row')
        self.main_frame.columnconfigure(0, weight=1)
        
        self.canvas_frame = self.canvas.create_window(0,0, window=self.main_frame, anchor="nw",            #add view port frame to canvas
                                  tags="self.main_frame")
        self.main_frame.bind("<Configure>", self.onFrameConfigure) 
        
        footer_frame = Frame(self)
        footer_frame.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(1, weight=1)
        footer_frame.grid(sticky=E + W)

        text = "All rights reserved"
        msg = Message(footer_frame, text=text)
        msg.config(font=NORM_FONT, width=w)
        msg.grid(row=0, column=0, sticky=W)
        
        link = create_link(footer_frame, "https://www.example.com", w)
        link.grid(row=0, column=1, sticky=E)
        
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
        
    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))     

        
def quit_application(x):
    root.quit()


root.withdraw()  # hide root window

# The welcome GUI
account_window = AccountWindow(root)
account_window.bind('<Destroy>', quit_application) 

# The register GUI
register_window = RegisterWindow(root)
register_window.bind('<Destroy>', quit_application)
register_window.withdraw()  

# The login GUI
login_window = LoginWindow(root)
login_window.bind('<Destroy>', quit_application)
login_window.withdraw()  

# The main GUI
admin_window = AdminWindow(root, int(0.7 * w), int(0.7 * h), int(0.15 * w), int(0.15 * h))
move_to_center(admin_window)
admin_window.bind('<Destroy>', quit_application)
admin_window.withdraw()  

#function to be called when user clicks on "Login"
def goto_login():
    account_window.unbind('<Destroy>')
    account_window.destroy()
    login_window.deiconify() # show login window
    
#function to be called when user clicks on "Register"
def goto_register():
    account_window.unbind('<Destroy>')
    account_window.destroy()
    register_window.deiconify() # show register window

#function to be called after user registration success  
def login_register():
    register_window.unbind('<Destroy>')
    register_window.destroy()
    login_window.deiconify() 
    
#function to save user credentials in .txt file
def register_user():
 
# get username and password
    username_info = username.get()
    password_info = password.get()
 
# Open file in write mode
    file = open(username_info + '.txt', "w")
 
# write username and password information into file
    file.write(username_info  + "\n")
    file.write(password_info)
    file.close()
 
    #register_window._username_entry.configure(state='disabled')
    #register_window._password_entry.configure(state='disabled')
 
# set a label for showing success information on screen 
    
    Label(register_window.entries_frame, text="Registration Success", fg="green", font=("calibri", 11)).grid(row = 2, column = 1)
    register_window._register_button.configure(text="Login")
    register_window._register_button.configure(command=login_register)
    
    CreateToolTip(register_window._register_button, text = 'Registration Success ! Click this \n'
                 'button to login to your account.')
    

# function to be called after success login  
def login_verification():
    
    login_window.unbind('<Destroy>')
    login_window.destroy()
    admin_window.deiconify() # show main window
  
# function to be called when user choose to logout
def logout():
    
    admin_window.unbind('<Destroy>')
    admin_window.destroy()
    account_window = AccountWindow(root)
    account_window.bind('<Destroy>', quit_application) 
    account_window.deiconify() # show welcome window

# function to be called when user clicks on cancel
def cancel():
    
    account_window = AccountWindow(root)
    account_window.bind('<Destroy>', quit_application) 
    account_window.deiconify() 
    
#function to be called when user clicks on "FILE"
def open_file():
    
    fname = sg.PopupGetFile(
        "Select a file to open:",
        title="Admin",
        file_types=(
            ("PDF files", "*.pdf"),
            ("WORD files", ["*.docx*", "*.doc*"]),
            #("Scanned files(images)", "*.jpg*"),
            # add more document types here
        ),
        icon=icon,
    )
    
    if fname:
        progress = ttk.Progressbar(admin_window.main_frame, orient=HORIZONTAL,
                               length=w, mode='determinate')
        
        msg = Message(admin_window.main_frame, text="Your file is being opened, please wait ...",justify='center', width=w, background="white",fg="#020769",font=("Helvetica", 18,"bold"))
        msg.grid(sticky=S, pady=30)
        progress.grid(sticky=N, pady=50)
        progress['value'] = 10
        admin_window.update_idletasks()
        progress['value'] = 20
        admin_window.update_idletasks()
        
        # define the name of the directory to be created and that contains the chosen files
        date_name = Path(fname).resolve().stem  + "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = Path(fname).absolute().parents[0] / date_name 
        
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            print ("Creation of the directory %s failed" % path)
            
        # copy file to the created directory
        shutil.copy(fname, path)
        
        if fname.lower().endswith(".pdf"):
            fname = path / Path(fname).name
            
        # if the chosen file is WORD file, convert to pdf using doc_to_pdf function of the pdf module
        elif fname.lower().endswith(".docx") or fname.lower().endswith(".doc"):
            fname = pdf.doc_to_pdf(fname, path)
            
        progress['value'] = 30
        admin_window.update_idletasks()
        
        progress['value'] = 40
        admin_window.update_idletasks()
        
        progress['value'] = 50
        admin_window.update_idletasks()
        
        progress['value'] = 60
        admin_window.update_idletasks()
        
        progress['value'] = 70
        admin_window.update_idletasks()
        
        progress['value'] = 80
        admin_window.update_idletasks()
        
        progress['value'] = 90
        admin_window.update_idletasks()
        
        progress['value'] = 100
        
        progress.grid_remove()
        msg.grid_remove()
        
        display_pdf(fname, icon, w, max_size)
            
    else:
        sg.Popup("Cancelling : ", "You have not chosen a file ! ", icon=icon)

     
# set handlers
account_window._register_button.configure(command=goto_register)
account_window._login_button.configure(command=goto_login)
register_window._register_button.configure(command=register_user)
register_window._cancel_button.configure(command=cancel)
login_window._login_button.configure(command=login_verification)
login_window._cancel_button.configure(command=cancel)
admin_window._logout_button.configure(command=logout)
admin_window._file_button.configure(command=open_file)


root.mainloop()
