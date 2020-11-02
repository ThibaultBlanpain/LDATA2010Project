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


from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter import colorchooser

import sys



fenetre = Tk()
fenetre.geometry("")
fenetre.title("Information Visualisation")

global canvas
MajorData = None

# ReadFile fonctionnel (pour ios en tous cas)
def ReadFile():
    filename = askopenfilename(title="Ouvrir votre document",filetypes=[('csv files','.csv'),('all files','.*')])
    fichier = pd.read_csv(filename,sep=r'\s*,\s*')
    print("file opened")
    MajorData = fichier
    return
buttonRead = Button(fenetre, text="Import Data from *.csv", command=ReadFile).grid(row = 0, column = 3, sticky = W, columnspan = 2)


# ClearData fonctionnel (meme si je pense qu'on override les previous data en faisant un deuxieume ReadFile)
def ClearData():
    MajorData = None
    return
button = Button(fenetre, text="Clear Imported Data from *.csv", command=ClearData).grid(row = 0, column = 5, sticky = W, columnspan = 2)


# bouton de sortie fonctionnel
def ExitTotal():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        fenetre.destroy()
    fenetre.quit()
    sys.exit()
    return None
boutonExit=Button(fenetre, text="Close", command=ExitTotal).grid(row = 0, column = 7, sticky = W, columnspan = 2)

#test plot

def ploterT(colnum):
    btn = Label(fenetre, text="specify plot title")
    btn.grid(row=1, column=colnum, padx=20, pady=10)
    
    x = ['Col A', 'Col B', 'Col C']
    y = [50, 20, 80]
    
    fig = plt.figure(figsize=(4, 5))
    plt.bar(x=x, height=y)
    
    # specify the window as master
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=colnum, ipadx=40, ipady=20)
    
    # navigation toolbar
    toolbarFrame = Frame(master=fenetre)
    toolbarFrame.grid(row=3,column=colnum)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

#(rgb, hx) = colorchooser.askcolor()
#print(rgb, hx)

def clearPloter():
    
    return

###################################################################
###################################################################
# besoin de definir toutes les fonctions au dessus des menubutton
###################################################################
###################################################################
# menu des fonctions display, faut plus que les fonctions
# Create a menu button
menubutton = Menubutton(fenetre, text="Display with")
menubutton.grid()
# Create pull down menu
menubutton.menu = Menu(menubutton, tearoff = 0)
menubutton["menu"] = menubutton.menu
# Add some commands
menubutton.menu.add_command(label="Force-Layout", command=ReadFile)
menubutton.menu.add_command(label="Networkx", command=lambda: ploterT(20))
menubutton.menu.add_command(label="Infection map", command=clearPloter)
menubutton.menu.add_command(label="Adjacency matrix")
menubutton.menu.add_command(label="Number of interactions")
menubutton.menu.add_command(label="caracteristics of the plot blabla")
menubutton.menu.add_separator()
menubutton.menu.add_command(label="Exit")
menubutton.grid(row=0, column=0)



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

fenetre.mainloop()