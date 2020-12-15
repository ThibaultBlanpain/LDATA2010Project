import matplotlib.pyplot as plt 
import networkx as nx 
import numpy as np 
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns 

import tkinter as tk 
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter import colorchooser
from tkinter.constants import *
from tkinter import font as tkFont
import sys

root = tk.Tk()



user_input1 = tk.StringVar(root)
user_input2 = tk.StringVar(root)
user_input3 = tk.StringVar(root)
user_input4 = tk.StringVar(root)
answer = 3

def verify(u):
    b = u.get()
    print(b)
    print(int(b) == answer)  # calling get() here!


def ExitTotal():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
    root.quit()
    sys.exit()
    return None


def defilGest(L):
    op, deCombien = L[0], L[1]

    if op == 'scroll':
        units = L[2]
        saisi.xview_scroll(deCombien, units)
    elif op == 'moveto':
        saisi.xview_moveto(deCombien)

# saisi = Entry(root, width=10)
# saisi.grid(row=0, column = 3, sticky='ew')

# saisiDefil = Scrollbar(root, orient='horizontal',
#     command=defilGest)
# saisiDefil.grid(row=1, column = 3, sticky='ew')

# saisi['xscrollcommand'] = saisiDefil.set

entry1 = tk.Entry(root,textvariable=user_input1).grid(row = 3, column = 9)
entry2 = tk.Entry(root,textvariable=user_input2).grid(row = 3, column = 9)
print(entry1, "fcfc")
check = tk.Button(root, text='check 3', command=lambda arg1   = user_input1 : verify(arg1))
check.grid(row = 2, column = 4)

# entry2 = tk.Entry(root, textvariable=user_input2)
# entry2.pack()
# check = tk.Button(root, text='check 3', command=lambda arg1   = user_input2 : verify(arg1))
# check.pack()

# entry3 = tk.Entry(root, textvariable=user_input3)
# entry3.pack()
# check = tk.Button(root, text='check 3', command=lambda arg1   = user_input3 : verify(arg1))
# check.pack()


boutonExit=Button(root, text="Close", command=ExitTotal).grid(row = 11, column = 1, sticky = W, columnspan = 1)



root.mainloop()




























# import tkinter as tk 
# from tkinter import ttk
# from tkinter.messagebox import *
# from tkinter.filedialog import *
# from tkinter.ttk import *
# from tkinter import colorchooser
# from tkinter.constants import *
# from tkinter import font as tkFont

# root = tk.Tk()

# user_input = tk.StringVar(root)
# user_input1 = tk.StringVar(root)
# user_input2 = tk.StringVar(root)
# user_input3 = tk.StringVar(root)
# user_input4 = tk.StringVar(root)
# answer = 3

# def verify(u):
#     b = u.get()
#     print(b)
#     print(int(b) == answer)  # calling get() here!



# def display_checked():
#     '''check if the checkbuttons have been toggled, and display 
#     a value of '1' if they are checked, '0' if not checked'''
#     red = red_var.get()
#     yellow = yellow_var.get()
#     green = green_var.get()
#     blue = blue_var.get()
 
#     print("red: {}\nyellow:{}\ngreen: {}\nblue: {}".format(
#         red, yellow, green, blue))
 
# # Create label
# label = tk.Label(root, text="Which colors do you like below?")
# label.grid(row=0)
 
# # Create variables and checkbuttons 
# red_var = tk.IntVar()
# tk.Checkbutton(root, width=10, text="red", variable=red_var, bg="red").grid(row=1)
# yellow_var = tk.IntVar()
# tk.Checkbutton(root, width=10, text="yellow", variable=yellow_var, bg="yellow").grid(row=2)
# green_var = tk.IntVar()
# tk.Checkbutton(root, width=10, text="green", variable=green_var, bg="green").grid(row=3)
# blue_var = tk.IntVar()
# tk.Checkbutton(root, width=10, text="blue", variable=blue_var, bg="blue").grid(row=4)

# entry = tk.Entry(root, textvariable=user_input4).grid(row = 2, column = 3)
# menubutton = Menubutton(root, text="Change values of variables")#, activebackground='red')
# menubutton.grid(row = 10, column = 1, sticky = 'ew', columnspan = 1)
# # # Create pull down menu
# menubutton.menu = Menu(menubutton, tearoff = 0, bg="red")
# menubutton["menu"] = menubutton.menu
# # # Add some commands
# menubutton.menu.add_command(label="in the main window", command=lambda arg1 = user_input4: verify(arg1))

# entry = tk.Entry(root, textvariable=user_input)
# entry.pack()
# #command=lambda arg1 = "the main window", arg2 = "po" : ploterT(arg1, arg2)
# check = tk.Button(root, text='check 3', command=lambda arg1 = user_input : verify(arg1))
# check.pack()

# entry1 = tk.Entry(root, textvariable=user_input1)
# entry1.pack()
# check = tk.Button(root, text='check 3', command=lambda arg1   = user_input1 : verify(arg1))
# check.pack()

# entry2 = tk.Entry(root, textvariable=user_input2)
# entry2.pack()
# check = tk.Button(root, text='check 3', command=lambda arg1   = user_input2 : verify(arg1))
# check.pack()

# entry3 = tk.Entry(root, textvariable=user_input3)
# entry3.pack()
# check = tk.Button(root, text='check 3', command=lambda arg1   = user_input3 : verify(arg1))
# check.pack()

