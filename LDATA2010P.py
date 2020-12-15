#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 22:27:53 2020

@author: thibaultblanpain
"""
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

# dash

fenetre = tk.Tk()
fenetre.title("Information Visualisation")
#networkx->degmin,widthmin,timestart,timeend,k,ite + bouton homeloc/shortest path
#map->timestart,timeend,nbrmin,sizeref
#barchart->timemin,timemax
#adjMatr->timemin,timemax

MAX_DISPLACEMENT_SQUARED = 10000
L = 50 #spring rest length
K_r = 2000 #repulsive force constant
K_s = 1  #spring constant
delta_t = 0.004 # time step


L = tk.StringVar(fenetre)
MAX_DISPLACEMENT_SQUARED = tk.StringVar(fenetre)
K_r = tk.StringVar(fenetre)
K_s = tk.StringVar(fenetre)
delta_t = tk.StringVar(fenetre)

def get_the_parameters():
    
    return


#boutonPlot_Caracteristics=Button(fenetre, text="caracteristics of the plot blabla", command=lambda arg1 = "the main window", arg2 = "Caracteristics of the plot" : ploterT(arg1, arg2)).grid(row = 9, column = 1, sticky = W, columnspan = 1)




global canvas
MajorData = None

fontt = tkFont.Font(family='Helvetica', size=36, weight='bold')

# ReadFile fonctionnel (pour ios en tous cas)
def ReadFile():
    filename = askopenfilename(title="Ouvrir votre document",filetypes=[('csv files','.csv'),('all files','.*')])
    fichier = pd.read_csv(filename,sep=r'\s*,\s*')
    print("file opened")
    MajorData = fichier
    return


# ClearData fonctionnel (meme si je pense qu'on override les previous data en faisant un deuxieume ReadFile)
def ClearData():
    MajorData = None
    return


# bouton de sortie fonctionnel
def ExitTotal():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        fenetre.destroy()
    fenetre.quit()
    sys.exit()
    return None

wherePP = "sb"

def where(place):
    global wherePP 
    wherePP = place
    if wherePP == "remove the graphs":
        plt.close("all")
    return

def AdjacencyMatrix(df,title,timemin,timemax):
    M=len(df['person1'])
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    data=np.zeros((N,N))
    for i in range(M):
        if((df['timestep'][i]>=timemin)and(df['timestep'][i]<=timemax)):
            p1=df['person1'][i]
            p2=df['person2'][i]
            data[p1][p2]=(data[p1][p2])+1
            data[p2][p1]=(data[p2][p1])+1
    
    az=sns.clustermap(
        vmin=0.0,
        vmax=data.max(),
        data=data,
        cmap="viridis_r",
        linewidths=0.0,
        mask=(data==0),
  )
    az.fig.suptitle('Adjacency matrix') 
    
    danslafen(title,az.fig)

#test plot
whereplot = "zero"
def ploterT(whereplot, title):
    global wherePP
    btn = Label(fenetre, text=title)
    btn.grid(row=1, column=10, padx=20, pady=10)
    x = ['Col A', 'Col B', 'Col C']
    y = [50, 20, 80]
    if title == "po":
        x = ['Col A', 'Col B', 'Col C', 'col D']
        y = [0, 0, 300, 80]
    fig = plt.figure(figsize=(3, 3))
    plt.bar(x=x, height=y)
    
    # specify the window as master
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=7, rowspan = 7, columnspan = 7, ipadx=70, ipady=70, sticky="nsew")#, padx=40, pady=40, ipadx=40, ipady=40, sticky= E, rowspan = 1, columnspan = 3)
    
    
    # navigation toolbar
    toolbarFrame = Frame(master=fenetre)
    toolbarFrame.grid(row=11,column=10, columnspan = 3)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    #toolbar.update()
    #canvas.get_tk_widget().pack()
    if wherePP == "the main window and another window":
        return
    if wherePP == "another window":
        btn3 = Label(fenetre, text=title)
        btn3.grid(row=13, column=1, padx=20, pady=10)
        #for item in canvas.get_tk_widget().find_all():
        canvas.get_tk_widget().pack_forget()
        return
    if wherePP == "the main window":
        plt.close()
    if wherePP == "remove the graphs":
        canvas = None
        btn2 = Label(fenetre, text=title)
        btn2.grid(row=13, column=1, padx=20, pady=10)
        plt.close("all")
        return

def verify(u):
    b = u.get()
    print(b)
    print(int(b) == answer)  # calling get() here!
answer = 3

#networkx->degmin,widthmin,timestart,timeend,k,ite + bouton homeloc/shortest path
#map->timestart,timeend,nbrmin,sizeref
#barchart->timemin,timemax
#adjMatr->timemin,timemax



def valid(arg1, arg2, arg3, arg4, arg5, arg6):
    global degmin,widthmin,timestart,timeend,k,ite,timestart,timeend,nbrmin,sizeref,timemin,timemax
    #,timemin,timemax
    
    if arg3 == None:
        timemin = int(arg1.get())
        timemax = int(arg2.get())
        print(timemin,timemax)
        return
    
    if arg5 == None:
        timestart = int(arg1.get())
        timeend = int(arg2.get())
        nbrmin = int(arg3.get())
        sizeref = int(arg4.get())
        print(timestart,timeend,nbrmin,sizeref)
        return
    
    degmin = int(arg1.get())
    widthmin = int(arg2.get())
    timestart = int(arg3.get())
    timeend = int(arg4.get())
    k = int(arg5.get())
    ite = int(arg6.get())
    print(degmin,widthmin,timestart,timeend,k,ite)
    

val = Button(fenetre, text='enchant')

def ess(func):
    
    global val
    if val != None:
        val.destroy()
        
    
    if(func == "networkx"):
        user_inputdeg = tk.StringVar(fenetre)
        user_inputwid = tk.StringVar(fenetre)
        user_inputtimS = tk.StringVar(fenetre)
        user_inputtimE = tk.StringVar(fenetre)
        user_inputk = tk.StringVar(fenetre)
        user_inputite = tk.StringVar(fenetre)
        
        # entry1 = tk.Entry(fenetre, textvariable=user_input1).grid(row = 12, column = 1)
        # check = tk.Button(fenetre, text='check 3', command=lambda arg1   = user_input1 : verify(arg1))
        # check.grid(row = 13, column = 1)
        
        DeMin = Label(fenetre, text = "Minimal degree").grid(row=13,column=1,sticky=W)
        Lam = Label(fenetre, text = "Minimal width").grid(row=14,column=1,sticky=W)
        TS = Label(fenetre, text = "Starting time").grid(row=15,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time").grid(row=16,column=1,sticky=W)
        kK = Label(fenetre, text = "K value").grid(row=17,column=1,sticky=W)
        ITE = Label(fenetre, text = "Number of iter").grid(row=18,column=1,sticky=W)
        
        degmin = tk.Entry(fenetre, textvariable=user_inputdeg, width=8).grid(row = 13, column = 1, sticky=E)
        widthmin = tk.Entry(fenetre,textvariable=user_inputwid, width=8).grid(row = 14, column = 1, sticky=E)
        timestart = tk.Entry(fenetre, textvariable=user_inputtimS, width=8).grid(row = 15, column = 1, sticky=E)
        timeend = tk.Entry(fenetre, textvariable=user_inputtimE, width=8).grid(row = 16, column = 1, sticky=E)
        k = tk.Entry(fenetre,textvariable=user_inputk, width=8).grid(row = 17, column = 1, sticky=E)
        ite = tk.Entry(fenetre,textvariable=user_inputite, width=8).grid(row = 18, column = 1, sticky=E)
        
        
        val = Button(fenetre, text='validate', command=lambda arg1 = user_inputdeg, arg2 = user_inputwid, arg3 = user_inputtimS, arg4 = user_inputtimE, arg5 = user_inputk, arg6 = user_inputite : valid(arg1,arg2, arg3, arg4, arg5, arg6))
        val.grid(row = 19, column = 1)
        
        
    if(func == "Infection map"):
        user_inputtimS = tk.StringVar(fenetre)
        user_inputtimE = tk.StringVar(fenetre)
        user_inputtimNbrm = tk.StringVar(fenetre)
        user_inputtimSizer = tk.StringVar(fenetre)
        
        TS = Label(fenetre, text = "Starting time").grid(row=13,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time").grid(row=14,column=1,sticky=W)
        NM = Label(fenetre, text = "Minimal number").grid(row=15,column=1,sticky=W)
        SR = Label(fenetre, text = "Size of reference").grid(row=16,column=1,sticky=W)
        
        timestart = tk.Entry(fenetre, textvariable=user_inputtimS, width=8).grid(row = 13, column = 1, sticky=E)
        timeend = tk.Entry(fenetre,textvariable=user_inputtimE, width=8).grid(row = 14, column = 1, sticky=E)
        nbrmin = tk.Entry(fenetre, textvariable=user_inputtimNbrm, width=8).grid(row = 15, column = 1, sticky=E)
        sizeref = tk.Entry(fenetre, textvariable=user_inputtimSizer, width=8).grid(row = 16, column = 1, sticky=E)
        
        val = Button(fenetre, text='validate', command=lambda arg1 = user_inputtimS, arg2 = user_inputtimE, arg3 = user_inputtimNbrm, arg4 = user_inputtimSizer, arg5 = None, arg6 = None : valid(arg1,arg2, arg3, arg4, arg5, arg6))
        val.grid(row = 17, column = 1)
    
    if(func == "Number of interactions"): #(modify color)
        user_inputtimMi = tk.StringVar(fenetre)
        user_inputtimMa = tk.StringVar(fenetre)
        
        TS = Label(fenetre, text = "Starting time").grid(row=13,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time").grid(row=14,column=1,sticky=W)
        
        timestart = tk.Entry(fenetre, textvariable=user_inputtimMi, width=8).grid(row = 13, column = 1, sticky=E)
        timeend = tk.Entry(fenetre,textvariable=user_inputtimMa, width=8).grid(row = 14, column = 1, sticky=E)
        
        val = Button(fenetre, text='validate', command=lambda arg1 = user_inputtimMi, arg2 = user_inputtimMa, arg3 = None, arg4 = None, arg5 = None, arg6 = None : valid(arg1,arg2, arg3, arg4, arg5, arg6))
        val.grid(row = 15, column = 1)
    
    if(func == "Adjacency matrix"):
        user_inputtimMi = tk.StringVar(fenetre)
        user_inputtimMa = tk.StringVar(fenetre)
        
        TS = Label(fenetre, text = "Starting time").grid(row=13,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time").grid(row=14,column=1,sticky=W)
        
        timestart = tk.Entry(fenetre, textvariable=user_inputtimMi, width=8).grid(row = 13, column = 1, sticky=E)
        timeend = tk.Entry(fenetre,textvariable=user_inputtimMa, width=8).grid(row = 14, column = 1, sticky=E)
        
        val = Button(fenetre, text='validate', command=lambda arg1 = user_inputtimMi, arg2 = user_inputtimMa, arg3 = None, arg4 = None, arg5 = None, arg6 = None : valid(arg1,arg2, arg3, arg4, arg5, arg6))
        val.grid(row = 15, column = 1)
    
    # user_input1 = tk.StringVar(fenetre)
    # entry1 = tk.Entry(fenetre, textvariable=user_input1).grid(row = 12, column = 1)
    # check = tk.Button(fenetre, text='check 3', command=lambda arg1   = user_input1 : verify(arg1))
    # check.grid(row = 13, column = 1)

#(rgb, hx) = colorchooser.askcolor()
#print(rgb, hx)
# dash

###################################################################
###################################################################
# besoin de definir toutes les fonctions au dessus des menubutton
###################################################################
###################################################################
# menu des fonctions display, faut plus que les fonctions
# Create a menu button
# menubutton = Menubutton(fenetre, text="How to display the graph?")#, activebackground='red')
# menubutton.grid(row = 1, column = 1, sticky = W, columnspan = 2)
# # # Create pull down menu
# menubutton.menu = Menu(menubutton, tearoff = 0, bg="red")
# menubutton["menu"] = menubutton.menu
# # Add some commands
# menubutton.menu.add_command(label="Adjacency matrix")
# menubutton.menu.add_command(label="Number of interactions")
# menubutton.menu.add_command(label="caracteristics of the plot blabla")
# menubutton.menu.add_separator()
# menubutton.menu.add_command(label="Exit")
# menubutton.grid(row=0, column=0)

Separator(fenetre, orient=VERTICAL).grid(column=2, row=0, rowspan=20, sticky='ns')
ttk.Sizegrip()


buttonRead = Button(fenetre, text="Import Data from *.csv", command=ReadFile)
buttonRead.grid(row = 2, column = 1, sticky = W, columnspan = 1)

buttonClear = Button(fenetre, text="Clear Imported Data", command=ClearData).grid(row = 3, column = 1, sticky = W, columnspan = 1)

boutonNextworkx=Button(fenetre, text="Networkx", command=lambda arg1 = "the main window", arg2 = "po" : ploterT(arg1, arg2)).grid(row = 4, column = 1, sticky = W, columnspan = 1)

boutonForce_Layout=Button(fenetre, text="Force-Layout", command=lambda arg1 = "the main window", arg2 = "Force-Layout" : ploterT(arg1, arg2)).grid(row = 5, column = 1, sticky = W, columnspan = 1)

boutonInfection_Map=Button(fenetre, text="Infection map", command=lambda arg1 = "the main window", arg2 = "Infection map" : ploterT(arg1, arg2)).grid(row = 6, column = 1, sticky = W, columnspan = 1)

boutonAdjacency_Matrix=Button(fenetre, text="Adjacency matrix", command=lambda arg1 = "the main window", arg2 = "Adjacency matrix" : ploterT(arg1, arg2)).grid(row = 7, column = 1, sticky = W, columnspan = 1)

boutonIntercation_Number=Button(fenetre, text="Number of interactions", command=lambda arg1 = "the main window", arg2 = "Number of interaction" : ploterT(arg1, arg2)).grid(row = 8, column = 1, sticky = W, columnspan = 1)


menubutton = Menubutton(fenetre, text="Modify parameters of ")#, activebackground='red')
menubutton.grid(row = 9, column = 1, sticky = 'ew', columnspan = 1)
# # Create pull down menu
menubutton.menu = Menu(menubutton, tearoff = 0)
menubutton["menu"] = menubutton.menu
# # Add some commands
menubutton.menu.add_command(label="the network", command=lambda arg1 = "networkx": ess(arg1))
menubutton.menu.add_command(label="the graph of the infection map", command=lambda arg1 = "Infection map": ess(arg1))
menubutton.menu.add_command(label="the of the number of interactions barchart", command=lambda arg1 = "Number of interactions": ess(arg1))
menubutton.menu.add_command(label="the adjacency matrix", command=lambda arg1 = "Adjacency matrix": ess(arg1))





#boutonPlot_Caracteristics=Button(fenetre, text="caracteristics of the plot blabla", command= lambda arg1 = "networkx" : ess(arg1)).grid(row = 9, column = 1, sticky = W, columnspan = 1)



menubutton = Menubutton(fenetre, text="How to display the graph?")#, activebackground='red')
menubutton.grid(row = 10, column = 1, sticky = 'ew', columnspan = 1)
# # Create pull down menu
menubutton.menu = Menu(menubutton, tearoff = 0, bg="red")
menubutton["menu"] = menubutton.menu
# # Add some commands
menubutton.menu.add_command(label="in the main window", command=lambda arg1 = "the main window": where(arg1))
menubutton.menu.add_command(label="in another window", command=lambda arg1 = "another window": where(arg1))
menubutton.menu.add_command(label="in the main window and in another window", command=lambda arg1 = "in the main window and in another window": where(arg1))
menubutton.menu.add_command(label="remove the graphs of other windows", command=lambda arg1 = "remove the graphs": where(arg1))

boutonExit=Button(fenetre, text="Close", command=ExitTotal).grid(row = 11, column = 1, sticky = W, columnspan = 1)



#fenetre.geometry('200x200')

col_count, row_count = fenetre.grid_size()
for col in range(col_count + 1):
    fenetre.grid_columnconfigure(col, minsize=40)
for row in range(row_count):
    fenetre.grid_rowconfigure(row, minsize=40)

# plot ideas:
# describe points plt.text(150, 6.5, r'Danger')
# legende of curves plt.plot(x, y, "g", linewidth=0.8, marker="+", label="Trajet 2")
# plt.legend()
# arrow toward point plt.annotate('Limite', xy=(150, 7), xytext=(165, 5.5), 
# arrowprops={'facecolor':'black', 'shrink':0.05} )
# from: https://python.doctor/page-creer-graphiques-scientifiques-python-apprendre









# # entrée
# value = StringVar()
# value.set("texte par défaut")
# entree = Entry(fenetre, textvariable=value, width=30)
# entree.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # checkbutton
# bouton = Checkbutton(fenetre, text="Nouveau?")
# bouton.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # radiobutton
# value = StringVar()
# bouton1 = Radiobutton(fenetre, text="Oui", variable=value, value=1)
# bouton2 = Radiobutton(fenetre, text="Non", variable=value, value=2)
# bouton3 = Radiobutton(fenetre, text="Peut être", variable=value, value=3)
# bouton1.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# bouton2.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# bouton3.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # liste
# liste = Listbox(fenetre)
# liste.insert(1, "Force-Layout")
# liste.insert(2, "Networkx")
# liste.insert(3, "Infection map")
# liste.insert(4, "Adjacency matrix")
# liste.insert(5, "Number of interactions")
# liste.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # canvas
# canvas = Canvas(fenetre, width=150, height=120, background='yellow')
# ligne1 = canvas.create_line(75, 0, 75, 120)
# ligne2 = canvas.create_line(0, 60, 150, 60)
# txt = canvas.create_text(75, 60, text="Cible", font="Arial 16 italic", fill="blue")
# canvas.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # Scale
# value = DoubleVar()
# scale = Scale(fenetre, variable=value)
# scale.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # Cadres
# fenetre['bg']='white'
# # frame 1
# Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
# Frame1.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# # frame 2
# Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
# Frame2.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# # frame 3 dans frame 2
# Frame3 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
# Frame3.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# # Ajout de labels
# Label(Frame1, text="Frame 1").grid(row = 2, column = 0, sticky = W, columnspan = 2)
# Label(Frame2, text="Frame 2").grid(row = 2, column = 0, sticky = W, columnspan = 2)
# Label(Frame3, text="Frame 3",bg="white").grid(row = 2, column = 0, sticky = W, columnspan = 2)

# Paned window
#p = PanedWindow(fenetre, orient=HORIZONTAL)
# p.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# p.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# p.add(Label(p, text='Volet 2', background='white', anchor=CENTER) )
# p.add(Label(p, text='Volet 3', background='red', anchor=CENTER) )
# p..grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # Spinbox
# s = Spinbox(fenetre, from_=0, to=10)
# s.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # LabelFrame
# l = LabelFrame(fenetre, text="Titre de la frame")
# l.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# Label(l, text="A l'intérieure de la frame").grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # Alertes
# def callback():
#     if askyesno('Titre 1', 'Êtes-vous sûr de vouloir faire ça?'):
#         showwarning('Titre 2', 'Tant pis...')
#     else:
#         showinfo('Titre 3', 'Vous avez peur!')
#         showerror("Titre 4", "Aha")
# Button(text='Action', command=callback).grid(row = 2, column = 0, sticky = W, columnspan = 2)

# def callback2():
#     nbinter=[0]*N
#     for i in range(M):
#         nbinter[df['person1'][i]]=nbinter[df['person1'][i]]+1
#         nbinter[df['person2'][i]]=nbinter[df['person2'][i]]+1
#     index= sorted(range(N), key=lambda k: nbinter[k],reverse=True)
#     nbinter=sorted(nbinter,reverse=True)
    
#     plt.figure()
#     plt.title("Number of interactions")

#     for i in range(N):
#         plt.bar(str(index[i]),nbinter[i], align='center',color='blue')

# Button(text="Bar chart", command=callback2).grid(row = 2, column = 0, sticky = W, columnspan = 2)

# Alertes
# def alert():
#     showinfo("alerte", "Bravo!")
# menubar = Menu(fenetre)
# menu1 = Menu(menubar, tearoff=0)
# menu1.add_command(label="Creer", command=alert)
# menu1.add_command(label="Editer", command=alert)
# menu1.add_separator()
# menu1.add_command(label="Quitter", command=fenetre.quit)
# menubar.add_cascade(label="Fichier", menu=menu1)
# menu2 = Menu(menubar, tearoff=0)
# menu2.add_command(label="Couper", command=alert)
# menu2.add_command(label="Copier", command=alert)
# menu2.add_command(label="Coller", command=alert)
# menubar.add_cascade(label="Editer", menu=menu2)
# menu3 = Menu(menubar, tearoff=0)
# menu3.add_command(label="A propos", command=alert)
# menubar.add_cascade(label="Aide", menu=menu3)
# fenetre.config(menu=menubar)
# Button(text='menumenu', command=alert).grid(row = 2, column = 0, sticky = W, columnspan = 2)


# Grid
#for ligne in range(5):
#    for colonne in range(5):
#        Button(fenetre, text='L%s-C%s' % (ligne, colonne), borderwidth=1).grid(row=ligne, column=colonne)

#Button(fenetre, text='L1-C1', borderwidth=1).grid(row=1, column=1)
#Button(fenetre, text='L1-C2', borderwidth=1).grid(row=1, column=2)
#Button(fenetre, text='L2-C3', borderwidth=1).grid(row=2, column=3)
#Button(fenetre, text='L2-C4', borderwidth=1).grid(row=2, column=4)
#Button(fenetre, text='L3-C3', borderwidth=1).grid(row=3, column=3)

# Image
#photo = PhotoImage(file="ma_photo.png")
#canvas = Canvas(fenetre,width=350, height=200)
#canvas.create_image(0, 0, anchor=NW, image=photo)
#canvas.grid(row = 2, column = 0, sticky = W, columnspan = 2)

# # Get Value OK
# def recupere():
#     print(entree.get())
#     showinfo("Alerte", entree.get())
# value = StringVar()
# value.set("Valeur")
# entree = Entry(fenetre, textvariable=value, width=30)
# entree.grid(row = 2, column = 0, sticky = W, columnspan = 2)
# bouton = Button(fenetre, text="Valider", command=recupere)
# bouton.grid(row = 2, column = 0, sticky = W, columnspan = 2)


# ReadFile parfait (pour ios en tous cas)
# def ReadFile():
#     filename = askopenfilename(title="Ouvrir votre document",filetypes=[('csv files','.csv'),('all files','.*')])
#     fichier = pd.read_csv(filename,sep=r'\s*,\s*')
#     print(fichier)
#     return fichier

#df = ReadFile()

#Label(fenetre, text=content).grid(row = 2, column = 0, sticky = W, columnspan = 2)
# def get_values(Ok):
#     filename = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt'),('all files','.*')])
#     fichier = open(filename, "r")
#     if Ok:
#         content = fichier.read()
#         fichier.close()
#         Label(fenetre, text=content, command=get_values).grid(row = 2, column = 0, sticky = W, columnspan = 2)
#         return null
#     else:
#         content = fichier.read()
#         fichier.close()
#         Label(fenetre, text="content retrieved", command=get_values).grid(row = 2, column = 0, sticky = W, columnspan = 2)
#         return content

# events
# fonction appellée lorsque l'utilisateur presse une touche
# def clavier(event):
#     global coords

#     touche = event.keysym

#     if touche == "Up":
#         coords = (coords[0], coords[1] - 10)
#     elif touche == "Down":
#         coords = (coords[0], coords[1] + 10)
#     elif touche == "Right":
#         coords = (coords[0] + 10, coords[1])
#     elif touche == "Left":
#         coords = (coords[0] -10, coords[1])
#     # changement de coordonnées pour le rectangle
#     canvas.coords(rectangle, coords[0], coords[1], coords[0]+25, coords[1]+25)

# #création du canvas
# canvas = Canvas(fenetre, width=250, height=250, bg="ivory")
# #coordonnées initiales
# coords = (0, 0)
# #création du rectangle
# rectangle = canvas.create_rectangle(0,0,25,25,fill="violet")
# #ajout du bond sur les touches du clavier
# canvas.focus_set()
# canvas.bind("<Key>", clavier)
# #création du canvas
# canvas.grid(row = 2, column = 0, sticky = W, columnspan = 2)

def closeW():
    fenetre.close()

fenetre.geometry("750x600")
fenetre.mainloop()