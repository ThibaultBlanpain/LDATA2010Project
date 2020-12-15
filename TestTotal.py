# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:42:32 2020

@author: franc
"""

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


import tkinter as tk 
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter import colorchooser
from tkinter.constants import *
from tkinter import font as tkFont
import sys

import seaborn as sns 
from grave import plot_network
from grave.style import use_attributes
from matplotlib.colors import LogNorm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm

# dash

def bye(event):
    #fenetre.attributes("-fullscreen", False)
    fenetre.destroy()
    sys.exit()
fenetre = tk.Tk()
fenetre.title("Information Visualisation")
fenetre.attributes("-fullscreen", True)
fenetre.bind("<Escape>", bye)



MAX_DISPLACEMENT_SQUARED = 10000
L = 50 #spring rest length
K_r = 2000 #repulsive force constant
K_s = 1  #spring constant
delta_t = 0.004 # time step

"""
L = tk.StringVar(fenetre)
MAX_DISPLACEMENT_SQUARED = tk.StringVar(fenetre)
K_r = tk.StringVar(fenetre)
K_s = tk.StringVar(fenetre)
delta_t = tk.StringVar(fenetre)
"""
def get_the_parameters():
    
    return


#boutonPlot_Caracteristics=Button(fenetre, text="caracteristics of the plot blabla", command=lambda arg1 = "the main window", arg2 = "Caracteristics of the plot" : ploterT(arg1, arg2)).grid(row = 9, column = 1, sticky = W, columnspan = 1)


#networkx->degmin,widthmin,timestart,timeend,k,ite + bouton homeloc/shortest path
#map->timestart,timeend,nbrmin,sizeref
#barchart->timemin,timemax
#adjMatr->timemin,timemax

#variables globales
global canvas
wherePP = "the main window"
btn=None
MajorData = None
timestepmax=0
textvar= None 
arg=None
quelfig=0
nodata=1
opt=1
nsp=0
label1=None
button1=None
entry1=None
button2=None
entry2=None
label2=None
button3=None
entry3=None
label3=None
nodescolor={}
edgescolor={}
edgeswidth={}
nodebegin=None
nodeend=None




fontt = tkFont.Font(family='Helvetica', size=36, weight='bold')

# ReadFile fonctionnel (pour ios en tous cas)
def ReadFile():
    global MajorData
    global timestepmax
    global nodata
    filename = askopenfilename(title="Ouvrir votre document",filetypes=[('csv files','.csv'),('all files','.*')])
    fichier = pd.read_csv(filename,sep=r'\s*,\s*')
    print("file opened")
    MajorData = fichier
    timestepmax=MajorData['timestep'][len(MajorData['timestep'])-1]
    showbuttons()
    nodata=0
    return


# ClearData fonctionnel (meme si je pense qu'on override les previous data en faisant un deuxieume ReadFile)
def ClearData():
    global MajorData
    global nodata
    MajorData = None
    nodata=1
    return


# bouton de sortie fonctionnel
def ExitTotal():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        fenetre.destroy()
    fenetre.quit()
    sys.exit()
    return None



def where(place):
    global wherePP 
    wherePP = place
    if wherePP == "remove the graphs":
        plt.close("all")
    return


#test plot
whereplot = "zero"
def ploterT(whereplot, title):
    global wherePP
    global btn
    if(btn!=None):
        btn.destroy()
    btn = Label(fenetre, text=title)
    btn.grid(row=1, column=10, padx=20, pady=10)
    x = ['Col A', 'Col B', 'Col C']
    y = [50, 20, 80]
    if title == "po":
        y = [0, 0, 300]
    fig = plt.figure(figsize=(3, 3))
    plt.bar(x=x, height=y)
    
def danslafen(title,fig):
    
    global wherePP
    global btn
    if(btn!=None):
        btn.destroy()
    btn = Label(fenetre, text=title)
    btn.grid(row=1, column=10, padx=20, pady=10)
    if(fig==None):
        return;
    # specify the window as master
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=7, rowspan = 7, columnspan = 7, ipadx=70, ipady=70, sticky="nsew")#, padx=40, pady=40, ipadx=40, ipady=40, sticky= E, rowspan = 1, columnspan = 3)
    #canvas.get_tk_widget().pack(side="top",fill='both',expand=True)

    # navigation toolbar
    toolbarFrame = Frame(master=fenetre)
    toolbarFrame.grid(row=11,column=10, columnspan = 3)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    #toolbar.update()
    #canvas.get_tk_widget().pack()
    if wherePP == "the main window and another window":
        return
    if wherePP == "another window":
        #btn3 = Label(fenetre, text=title)
        #btn3.grid(row=13, column=1, padx=20, pady=10)
        #for item in canvas.get_tk_widget().find_all():
        canvas.get_tk_widget().pack_forget()
        return
    if wherePP == "the main window":
        plt.close()
        return
    if wherePP == "remove the graphs":
        canvas = None
        btn2 = Label(fenetre, text=title)
        btn2.grid(row=13, column=1, padx=20, pady=10)
        plt.close("all")
        return



#def waitcursor():
#    fenetre.config(cursor="watch")
#    fenetre.update()


def Networkx(df,title,degmin,widthmin,timestart,timeend,k,ite,infectedonly):
    destroyoptions()
    global nodata
    if(nodata==1):
        danslafen("No data",None)
        return;
    global arg
    global quelfig
    quelfig=1
    M=len(df['person1'])
    G=nx.Graph(name="Interaction Graph")
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    intdict={}
    for i in range(N):
        G.add_node(i,size=50,homelong=0,homelat=0,degtot=0)
    for i in range(M):
        if((df['timestep'][i]>=timestart) and (df['timestep'][i]<=timeend)):
            pers1=df['person1'][i]
            pers2=df['person2'][i]
            danger=0
            if (df['infected1'][i]!=df['infected2'][i]):
                danger=1
            if (pers1,pers2) in intdict.keys():
                if(intdict[(pers1,pers2)][1]==0):
                    intdict[(pers1,pers2)]= (intdict[(pers1,pers2)][0]+1,danger)
                else:
                    intdict[(pers1,pers2)]= (intdict[(pers1,pers2)][0]+1,1)
            else:
                intdict[(pers1,pers2)]= (1,danger)
    for key,value in intdict.items():
        if(value[0]>=widthmin):
            if(value[1]==1):
                G.add_edge(key[0],key[1],color='red',width=min((value[0]/10),5))
            else:
                if(infectedonly==0):
                    G.add_edge(key[0],key[1],color='black',width=min((value[0]/10),5))
    for i in range(M):
        G.nodes[df['person1'][i]]['homelong']=df['home1_long'][i]
        G.nodes[df['person1'][i]]['homelat']=df['home1_lat'][i]
        G.nodes[df['person2'][i]]['homelong']=df['home2_long'][i]
        G.nodes[df['person2'][i]]['homelat']=df['home2_lat'][i]
    for i in range(N):
        if(G.degree(i)<degmin):
            G.remove_node(i)
    d=dict(G.degree)
    for ke in d.keys():
        G.nodes[ke]['size'] = 5+3*d[ke]
    for kc in G.nodes(data=True):
        for neigh in G.neighbors(kc[0]):
            if (kc[0],neigh) in intdict:
                kc[1]['degtot']=kc[1]['degtot']+intdict[(kc[0],neigh)][0]
            else:
                kc[1]['degtot']=kc[1]['degtot']+intdict[(neigh,kc[0])][0]
    max_value=0
    for km in G.nodes(data=True):
        if(km[1]['degtot']>max_value):
            max_value=km[1]['degtot']
    blues = cm.get_cmap('Blues', 1000)
    for g in G.nodes(data=True):
        g[1]['color'] = blues(g[1]['degtot']/max_value)
    arg=G        
    carac()
    def spring_layout(networkx):
        pos = nx.spring_layout(G,k=k,iterations=ite)
        return pos
    plt.ion()
    fig, ax = plt.subplots()
    plt.title("Graph of interactions with networkx algorithm")
    #nx.draw(G,with_labels=True,font_weight='bold',edge_color=colors, width=weigths)
    art = plot_network(G, layout=spring_layout, ax=ax,node_style=use_attributes(), edge_style=use_attributes())
    #danslafen(title,fig)
    art.set_picker(10)
    fig.canvas.mpl_connect('pick_event', hilighter)
    
  
    
def hilighter(event):
    global nodescolor
    global edgescolor
    global edgeswidth
    global textvar
    # if we did not hit a node, bail
    if not hasattr(event, 'nodes') or not event.nodes:
        return

    graph = event.artist.graph
    global opt
    # clear any non-default color on nodes
    #for node, attributes in graph.nodes.data():
      #  attributes.pop('color', None)

    #for u, v, attributes in graph.edges.data():
      #  attributes.pop('width', None)
    if(opt==0): 
        for edge in edgescolor.keys():
            graph.edges[edge]['color']=edgescolor[edge]
            graph.edges[edge]['width']=edgeswidth[edge]
        edgescolor={}
        edgeswidth={}
        for node in nodescolor.keys():
            graph.nodes[node]['color'] = nodescolor[node]
        nodescolor={}
        for node in event.nodes:
            nodescolor[node]=graph.nodes[node]['color']
            graph.nodes[node]['color'] = 'red'

         
        for node in event.nodes:
          if(textvar!=None):
              textvar.remove()
          textvar=plt.text(0.7,0.7,'Home localisation \nid=%d \nlong=%f \nlat=%f' %(node,graph.nodes[node]['homelong'],graph.nodes[node]['homelat']),bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    global nsp
    global nodebegin
    global nodeend
    if(opt==1):  
        if(nsp==0):
            for edge in edgescolor.keys():
                graph.edges[edge]['color']=edgescolor[edge]
                graph.edges[edge]['width']=edgeswidth[edge]
            edgescolor={}
            edgeswidth={}
            for node in nodescolor.keys():
                graph.nodes[node]['color'] = nodescolor[node]
            nodescolor={}
            node=event.nodes[0]
            #nodescolor[node]=graph.nodes[node]['color']
            nodebegin=node
            #graph.nodes[node]['color'] = 'red'
            if(textvar!=None):
                textvar.remove()
            nsp=1
            textvar=plt.text(0.7,0.7,'select another node')
            
        else:
            node=event.nodes[0]
            nodeend=node
            shortestPath(graph,nodebegin,nodeend)
            if(textvar!=None):
                textvar.remove()
            nsp=0
            textvar=plt.text(0.7,0.7,'select a node')
            
            
    # update the screen
    event.artist.stale = True
    event.artist.figure.canvas.draw_idle()



def Map(df,title,timestart,timeend,nbrmin,sizeref):
    destroyoptions()
    global nodata
    if(nodata==1):
        danslafen("No data",None)
        return;
    M=len(df['person1'])
    start=0
    end=M
    ds=0
    de=0
    if(df['timestep'][end-1]==timeend):
        de=1
    for i in range(M):
        if ((df['timestep'][i]==timestart)and(ds==0)):
            start=i
            ds=1
        if((de==0)and(df['timestep'][i]==timeend)and(df['timestep'][i+1]>timeend)):
             end=i+1
    ntot=end-start

    BBox=(2.2468, 6.827,49.467,51.570)
    locdict={}
    map_m = plt.imread('belgium_map.png')
    fig=plt.figure()
    for i in range(start,end):
        x= df['loc_long'][i]
        y= df['loc_lat'][i]
        if (x,y) in locdict.keys():
            locdict[(x,y)]=locdict[(x,y)]+1
        else:
            locdict[(x,y)]=1
                
    for key,value in locdict.items():
        if(value>=nbrmin) :    
            plt.scatter(key[0], key[1], zorder=1, alpha= 1, c='black', s=value*sizeref/ntot)  
  
    plt.title('Interaction map')
    plt.xlim(BBox[0],BBox[1])
    plt.ylim(BBox[2],BBox[3])
    plt.imshow(map_m, zorder=0, extent=BBox, aspect=2)
    
    danslafen(title,fig)

def BarChart(df,title,timemin,timemax):
    destroyoptions()
    global nodata
    if(nodata==1):
        danslafen("No data",None)
        return;
    global quelfig
    quelfig=3
    global arg
    M=len(df['person1'])
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    nbinter=[0]*N
    for i in range(M):
        if((df['timestep'][i]>=timemin) and (df['timestep'][i]<=timemax)):
            nbinter[df['person1'][i]]=nbinter[df['person1'][i]]+1
            nbinter[df['person2'][i]]=nbinter[df['person2'][i]]+1
    arg=nbinter
    carac()
    index= sorted(range(N), key=lambda k: nbinter[k],reverse=True)
    nbinter=sorted(nbinter,reverse=True)

    fig=plt.figure()
    plt.title("Number of interactions of people")
    plt.xlabel("id")
    plt.ylabel("Intercations")
    for i in range(N):
        if(nbinter[i]!=0):
            plt.bar(str(index[i]),nbinter[i], align='center',color='blue')   

    
    danslafen(title,fig)

def AdjacencyMatrix(df,title,timemin,timemax):
    destroyoptions()
    global nodata
    if(nodata==1):
        danslafen("No data",None)
        return;
    global quelfig
    quelfig=4
    global arg
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
    arg=data
    carac()
    az=sns.clustermap(
        vmin=0.0,
        vmax=data.max(),
        data=data,
        cmap="viridis_r",
        linewidths=0.0,
        mask=(data==0),
        figsize=(5,5),
        xticklabels=True,
        yticklabels=True
        )
    az.fig.suptitle('Adjacency matrix') 
    
    danslafen(title,az.fig)

def Interplot(df,title):
    destroyoptions()
    global nodata
    if(nodata==1):
        danslafen("No data",None)
        return;
    global quelfig
    quelfig=5
    global arg
    M=len(df['person1'])
    T=df['timestep'].max()+1
    TimeI = [0]*T
    for i in range(M):
        if(df['infected1'][i]!=df['infected2'][i]):
            TimeI[df['timestep'][i]]=(TimeI[df['timestep'][i]])+1
    fig=plt.figure()
    plt.title("Interactions between infected and non-infected people")
    plt.xlabel("Timestep")
    plt.ylabel("Risky intercations")
    plt.plot(TimeI)
    
    arg=TimeI
    carac()
    
    danslafen(title,fig)


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
    
def caract(arg):
    global quelfig
    global label1
    global button1
    global entry1
    if(label1!=None):
        label1.destroy()
    if(button1!=None):
        button1.destroy()
    if(entry1!=None):
        entry1.destroy()
    if(quelfig==1):
        label1 = tk.Label(fenetre, text=nx.info(arg))
        label1.grid(row=12, column=1, padx=20, pady=10)
        moreoptions(arg)
    if(quelfig==5):
        entry1=tk.Entry(fenetre)
        entry1.grid(row=12,column=1,padx=20,pady=10)
        def getInter():
            global label1
            if(label1!=None):
                label1.destroy()
            x=int(entry1.get())
            label1 = tk.Label(fenetre, text=arg[x])
            label1.grid(row=13,column=1,padx=20,pady=10)
        button1 = tk.Button(text='Get number of risky interactions', command=getInter)
        button1.grid(row=14,column=1,padx=20,pady=10)
    if(quelfig==4):
        entry1=tk.Entry(fenetre)
        entry1.grid(row=12,column=1,padx=20,pady=10)
        def getInterx1x2(): 
            global label1
            if(label1!=None):
                label1.destroy()
            x=entry1.get().split(",")
            x1=int(x[0])
            x2=int(x[1])
            label1 = tk.Label(fenetre, text=arg[x1][x2])
            label1.grid(row=13,column=1,padx=20,pady=10)
        button1 = tk.Button(text="Format x1,x2", command=getInterx1x2)
        button1.grid(row=14,column=1,padx=20,pady=10)
    if(quelfig==3):
        entry1=tk.Entry(fenetre)
        entry1.grid(row=12,column=1,padx=20,pady=10)
        def getInterid():
            global label1
            if(label1!=None):
                label1.destroy()
            x=int(entry1.get())
            label1 = tk.Label(fenetre, text=arg[x])
            label1.grid(row=13,column=1,padx=20,pady=10)
        button1 = tk.Button(text='Get number interactions for id', command=getInterid)
        button1.grid(row=14,column=1,padx=20,pady=10)

def shortestPath(G,node1,node2):
    global nodescolor
    global edgescolor
    global edgeswidth
    path = nx.shortest_path(G,source=node1,target=node2)
    path_edges = zip(path,path[1:])
    for node in path:
        nodescolor[node]=G.nodes[node]['color']
        G.nodes[node]['color'] = 'yellow'
    for edge in path_edges:
        edgescolor[edge]=G.edges[edge]['color']
        edgeswidth[edge]=G.edges[edge]['width']
        G.edges[edge]['color']='yellow'
        G.edges[edge]['width']=5

def moreoptions(G):
    global button2
    global entry2
    global label2
    entry2=tk.Entry(fenetre)
    entry2.grid(row=1,column=4,padx=20,pady=10)
    def betwcen():
        global label2
        x=int(entry2.get())
        betw=nx.betweenness_centrality(G)
        if(label2!=None):
            label2.destroy()
        label2 = tk.Label(fenetre, text=betw[x])
        label2.grid(row=2,column=4,padx=20,pady=10)
    button2 = tk.Button(text='Betweenness centrality of n', command=betwcen)
    button2.grid(row=3,column=4,padx=20,pady=10)
    global button3
    global entry3
    global label3
    entry3=tk.Entry(fenetre)
    entry3.grid(row=4,column=4,padx=20,pady=10)
    def clustercoef():
        global label3
        x=int(entry3.get())
        clus=nx.clustering(G,x)
        if(label3!=None):
            label3.destroy()
        label3 = tk.Label(fenetre, text=clus)
        label3.grid(row=5,column=4,padx=20,pady=10)
    button3 = tk.Button(text='Clustering ceofficient n', command=clustercoef)
    button3.grid(row=6,column=4,padx=20,pady=10)

def destroyoptions():
    global button1
    global entry1
    global label1
    global button2
    global entry2
    global label2
    global button3
    global entry3
    global label3
    if(label1!=None):
        label1.destroy()
    if(button1!=None):
        button1.destroy()
    if(entry1!=None):
        entry1.destroy()
    if(button2!=None):
        button2.destroy()
        entry2.destroy()
        if(label2!=None):
            label2.destroy()
        button3.destroy()
        entry3.destroy()
        if(label3!=None):
            label3.destroy()

Separator(fenetre, orient=VERTICAL).grid(column=2, row=0, rowspan=40, sticky='ns')
ttk.Sizegrip()


buttonRead = Button(fenetre, text="Import Data from *.csv", command=ReadFile)
buttonRead.grid(row = 2, column = 1, sticky = W, columnspan = 1)

buttonClear = Button(fenetre, text="Clear Imported Data", command=ClearData).grid(row = 3, column = 1, sticky = W, columnspan = 1)
def showbuttons():
    boutonNextworkx=Button(fenetre, text="Graph (new window only)", command=lambda df=MajorData, title = "Graph", degmin=1,widthmin=1,timemin=0,timemax=timestepmax,k=0.1,iterations=50, infeconly=0 : Networkx(df,title,degmin,widthmin,timemin,timemax,k,iterations,infeconly)).grid(row = 4, column = 1, sticky = W, columnspan = 1)

    #boutonForce_Layout=Button(fenetre, text="Force-Layout", command=lambda arg1 = "the main window", arg2 = "Force-Layout" : ploterT(arg1, arg2)).grid(row = 5, column = 1, sticky = W, columnspan = 1)

    boutonInfection_Map=Button(fenetre, text="Interaction map", command=lambda df = MajorData, title = "Map of interactions" , timemin=0, timemax=50, nbremin=1, sizeref=10000: Map(df,title,timemin,timemax,nbremin,sizeref)).grid(row = 6, column = 1, sticky = W, columnspan = 1)

    boutonInteraction_people=Button(fenetre, text="Interaction/person", command=lambda df = MajorData, title = "Intercation/person" , timemin=0, timemax=timestepmax: BarChart(df,title,timemin,timemax)).grid(row = 5, column = 1, sticky = W, columnspan = 1)

    boutonAdjacency_Matrix=Button(fenetre, text="Adjacency matrix", command=lambda df = MajorData, title = "Adjacency matrix" ,timemin=0,timemax=timestepmax: AdjacencyMatrix(df,title,timemin,timemax)).grid(row = 7, column = 1, sticky = W, columnspan = 1)

    boutonIntercation_Number=Button(fenetre, text="Number of risky interactions", command=lambda df=MajorData, title = "Number of risky interactions" : Interplot(df, title)).grid(row = 8, column = 1, sticky = W, columnspan = 1)
def carac():
    boutonPlot_Caracteristics=Button(fenetre, text="Caracteristics of the plot ", command=lambda arg1 = arg : caract(arg1)).grid(row = 9, column = 1, sticky = W, columnspan = 1)



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