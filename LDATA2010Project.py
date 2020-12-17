# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 22:27:53 2020

@author: thibaultblanpain & francoisdawance
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
from sklearn import cluster



def bye(event):
    plt.close('all')
    fenetre.destroy()
    sys.exit()
fenetre = tk.Tk()
fenetre.title("Information Visualisation")
fenetre.attributes("-fullscreen", True)
fenetre.bind("<Escape>", bye)



#global variables
canvas=None
toolbarFrame=None
wherePP = "the main window"
btn=None
MajorData = None
timestepmax=0
textvar= None 
textvar2=None
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
button4=None
button5=None
entry5=None
button6=None
label7=None
entry7=None
button7=None
buttonopt=None
nodescolor={}
nodescolor2={}
todestroysp=[]
nodebegin=None
nodeend=None
listtodel=[]
G=None
posf=None



fontt = tkFont.Font(family='Helvetica', size=36, weight='bold')

#readfile
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
    danslafen("Data loaded!",None)
    return


# ClearData fonctionnel (meme si on override les previous data en faisant un deuxieume ReadFile)
def ClearData():
    global MajorData
    global nodata
    MajorData = None
    nodata=1
    danslafen("Data cleared!",None)
    destroyoptions(1)
    return


# bouton de sortie fonctionnel
def ExitTotal():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        fenetre.destroy()
    plt.close('all')
    fenetre.quit()
    sys.exit()
    return None



def where(place):
    global wherePP 
    wherePP = place
    if wherePP == "remove the graphs":
        plt.close("all")
    return


    
def danslafen(title,fig):
    
    global wherePP
    global btn
    global canvas
    global toolbarFrame
    if(btn!=None):
        btn.destroy()
    btn = Label(fenetre, text=title)
    btn.grid(row=1, column=10, padx=20, pady=10)
    if(fig==None):
        return;

    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=7, rowspan = 7, columnspan = 7, ipadx=70, ipady=70, sticky="nsew")

    toolbarFrame = Frame(master=fenetre)
    toolbarFrame.grid(row=11,column=10, columnspan = 3)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    if wherePP == "the main window and another window":
        return
    if wherePP == "another window":
        canvas.get_tk_widget().destroy()
        toolbarFrame.destroy()
        canvas.get_tk_widget().pack_forget()
        return
    if wherePP == "the main window":
        plt.close()
        return
    if wherePP == "remove the graphs":
        canvas = None
        plt.close("all")
        return



#def waitcursor():
#    fenetre.config(cursor="watch")
#    fenetre.update()


def Networkx(df,title,degmin,widthmin,timestart,timeend,k,ite,infectedonly,newplot):
    destroyoptions(newplot)
    global G
    global posf
    global textvar
    global textvar2
    global nodescolor
    global nodescolor2
    textvar=None
    textvar2=None
    nodescolor={}
    nodescolor2={}
    global nodata
    if(nodata==1):
        danslafen("No data!",None)
        return;
    danslafen("Graph",None)
    global arg
    global quelfig
    quelfig=1
    global buttonopt
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
            pers1=min(df['person1'][i],df['person2'][i])
            pers2=max(df['person1'][i],df['person2'][i])
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
    def changeopt():
        global opt
        global textvar
        global textvar2
        opt=1-opt
        if(textvar!=None):
            textvar.remove() 
        if(textvar2!=None):
            textvar2.remove()
        if(opt==1):
            textvar=plt.text(0.7,0.7,'select a node')
            textvar2=plt.text(0.7,0.8,'Shortest path',fontsize=12)
        if(opt==0):
            textvar2=plt.text(0.7,0.8,'Home localisation',fontsize=12)
            textvar=None
            
    
    buttonopt = tk.Button(text="Shortestpath/Home Localisation", command=changeopt)
    buttonopt.grid(row=5,column=6,padx=20,pady=10)
    posf=nx.spring_layout(G,k=k,iterations=ite)
    def spring_layout(networkx):
        return posf
    
    plt.ion()
    fig, ax = plt.subplots()
    plt.title("Graph of interactions with networkx algorithm")
    changeopt()  
    art = plot_network(G, layout=spring_layout, ax=ax,node_style=use_attributes(), edge_style=use_attributes())
    art.set_picker(10)
    fig.canvas.mpl_connect('pick_event', hilighter)
    
  
    
def hilighter(event):
    global nodescolor
    global textvar
    global todestroysp

    if not hasattr(event, 'nodes') or not event.nodes:
        return

    graph = event.artist.graph
    global opt
    if(opt==0): 
        while (todestroysp!=[]):
            if(todestroysp[0]!=None):
                todestroysp[0].remove()
            todestroysp.pop(0)
        for node in nodescolor.keys():
            graph.nodes[node]['color'] = nodescolor[node]
        nodescolor={}
        node = event.nodes[0]
        nodescolor[node]=graph.nodes[node]['color']
        graph.nodes[node]['color'] = 'red'
        if(textvar!=None):
            textvar.remove()
        textvar=plt.text(0.7,0.55,'Home localisation \nid=%d \nlong=%f \nlat=%f' %(node,graph.nodes[node]['homelong'],graph.nodes[node]['homelat']),bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    global nsp
    global nodebegin
    global nodeend
    if(opt==1):  
        if(nsp==0):          
            while (todestroysp!=[]):
                if(todestroysp[0]!=None):
                    todestroysp[0].remove()
                todestroysp.pop(0)
            for node in nodescolor.keys():
                graph.nodes[node]['color'] = nodescolor[node]
            nodescolor={}
            node=event.nodes[0]
            nodebegin=node
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



def Map(df,title,timestart,timeend,nbrmin,sizeref,newplot):
    destroyoptions(newplot)
    global nodata
    if(nodata==1):
        danslafen("No data!",None)
        return;
    global quelfig
    quelfig=2
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
    carac()
    plt.title('Interaction map')
    plt.xlim(BBox[0],BBox[1])
    plt.ylim(BBox[2],BBox[3])
    plt.imshow(map_m, zorder=0, extent=BBox, aspect=2)
    
    danslafen(title,fig)

def BarChart(df,title,timemin,timemax,orange,red,newplot):
    print(timemax)
    destroyoptions(newplot)
    global nodata
    if(nodata==1):
        danslafen("No data!",None)
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
    plt.ylabel("Interactions")
    for i in range(N):
        if(nbinter[i]!=0):
            if(nbinter[i]<orange):
                plt.bar(str(index[i]),nbinter[i], align='center',color='green') 
            elif(nbinter[i]>red):
                plt.bar(str(index[i]),nbinter[i], align='center',color='red')
            else:
                plt.bar(str(index[i]),nbinter[i], align='center',color='orange')
                

    
    danslafen(title,fig)

def AdjacencyMatrix(df,title,timemin,timemax,newplot):
    destroyoptions(newplot)
    global nodata
    if(nodata==1):
        danslafen("No data!",None)
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
    destroyoptions(1)
    global nodata
    if(nodata==1):
        danslafen("No data!",None)
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
    plt.ylabel("Risky interactions")
    plt.plot(TimeI)
    
    arg=TimeI
    carac()
    
    danslafen(title,fig)

    
def caract(new):
    global arg
    global quelfig
    global label1
    global button1
    global entry1
    ess(quelfig,new)
    if(label1!=None):
        label1.destroy()
    if(button1!=None):
        button1.destroy()
    if(entry1!=None):
        entry1.destroy()
    if(quelfig==1):
        label1 = tk.Label(fenetre, text=nx.info(arg))
        label1.grid(row=2, column=6, padx=20, pady=10)
        moreoptions(arg)
    if(quelfig==5):
        entry1=tk.Entry(fenetre)
        entry1.grid(row=12,column=4,padx=20,pady=10)
        def getInter():
            global label1
            if(label1!=None):
                label1.destroy()
            x=int(entry1.get())
            label1 = tk.Label(fenetre, text=arg[x])
            label1.grid(row=13,column=4,padx=20,pady=10)
        button1 = tk.Button(text='Get number of risky interactions', command=getInter)
        button1.grid(row=14,column=4,padx=20,pady=10)
    if(quelfig==4):
        entry1=tk.Entry(fenetre)
        entry1.grid(row=12,column=4,padx=20,pady=10)
        def getInterx1x2(): 
            global label1
            if(label1!=None):
                label1.destroy()
            x=entry1.get().split(",")
            x1=int(x[0])
            x2=int(x[1])
            label1 = tk.Label(fenetre, text=arg[x1][x2])
            label1.grid(row=13,column=4,padx=20,pady=10)
        button1 = tk.Button(text="Format x1,x2", command=getInterx1x2)
        button1.grid(row=14,column=4,padx=20,pady=10)
    if(quelfig==3):
        entry1=tk.Entry(fenetre)
        entry1.grid(row=12,column=4,padx=20,pady=10)
        def getInterid():
            global label1
            if(label1!=None):
                label1.destroy()
            x=int(entry1.get())
            label1 = tk.Label(fenetre, text=arg[x])
            label1.grid(row=13,column=4,padx=20,pady=10)
        button1 = tk.Button(text='Get number interactions for id', command=getInterid)
        button1.grid(row=14,column=4,padx=20,pady=10)
   

def shortestPath(G,node1,node2):
    global posf
    global nodescolor
    global todestroysp
    path = nx.shortest_path(G,source=node1,target=node2)
    path_edges = zip(path,path[1:])
    for node in path:
        nodescolor[node]=G.nodes[node]['color']
        G.nodes[node]['color'] = 'yellow'
    for edge in path_edges:
        b=nx.draw_networkx_edges(G,posf,edgelist=[edge],edge_color='yellow',width=5)
        todestroysp.append(b)
       
        
        
def moreoptions(G):
    global button2
    global entry2
    global label2
    entry2=tk.Entry(fenetre)
    entry2.grid(row=1,column=4,padx=20,pady=10,sticky=NW)
    def betwcen():
        global label2
        x=int(entry2.get())
        betw=nx.betweenness_centrality(G)
        if(label2!=None):
            label2.destroy()
        label2 = tk.Label(fenetre, text=betw[x])
        label2.grid(row=1,column=4,padx=20,pady=10,sticky=NE)
    button2 = tk.Button(text='Betweenness centrality of n', command=betwcen)
    button2.grid(row=2,column=4,padx=20,pady=10,sticky=NW)
    global button3
    global entry3
    global label3
    entry3=tk.Entry(fenetre)
    entry3.grid(row=4,column=4,padx=20,pady=10,sticky=NW)
    def clustercoef():
        global label3
        x=int(entry3.get())
        clus=nx.clustering(G,x)
        if(label3!=None):
            label3.destroy()
        label3 = tk.Label(fenetre, text=clus)
        label3.grid(row=4,column=4,padx=20,pady=10,sticky=NE)
    button3 = tk.Button(text='Clustering coefficient n', command=clustercoef)
    button3.grid(row=5,column=4,padx=20,pady=10,sticky=NW)
    global button4
    def mst():
        global G
        global posf
        global nodescolor
        for node in nodescolor.keys():
            G.nodes[node]['color'] = nodescolor[node]
        nodescolor={}
        plt.figure()
        T=nx.minimum_spanning_tree(G)
        arraycn=[]
        arraysn=[]
        for g in G.nodes(data=True):
            arraycn.append(g[1]['color'])
            arraysn.append(g[1]['size'])
        edges = T.edges()
        colorst = [G[u][v]['color'] for u,v in edges]
        widthst = [G[u][v]['width'] for u,v in edges]
        nx.draw(T,posf,node_size=arraysn,node_color=arraycn,edge_color=colorst,width=widthst)
    button4 = tk.Button(text='Minimum spanning tree', command=mst)
    button4.grid(row=8,column=6,padx=20,pady=10,sticky=NW)
    global button5
    global entry5
    entry5=tk.Entry(fenetre)
    entry5.grid(row=7,column=4,padx=20,pady=10,sticky=NW)
    def clusters():
        global G
        global nodescolor2
        global nodescolor
        global entry5
        for node in nodescolor.keys():
            G.nodes[node]['color'] = nodescolor[node]
        nodescolor={}
        for node in nodescolor2.keys():
            G.nodes[node]['color'] = nodescolor2[node]
        nodescolor2={}
        n_clus=1
        if(entry5!=None):
            n_clus=int(entry5.get())
        def graph_to_edge_matrix(G):
            edge_mat = np.zeros((len(G), len(G)), dtype=int)
            for node in G:
                for neighbor in G.neighbors(node):
                    edge_mat[node][neighbor] = 1
                edge_mat[node][node] = 1
            return edge_mat
        clus=cluster.KMeans(n_clus).fit(graph_to_edge_matrix(G))
        for node in nodescolor.keys():
            G.nodes[node]['color'] = nodescolor[node]
        nodescolor={}
        rb = cm.get_cmap('rainbow', 1000)
        for node in G.nodes(data=True):
            nodescolor2[node[0]]=node[1]['color']
            node[1]['color'] = rb(clus.labels_[node[0]]/n_clus)
    button5=tk.Button(text="Clusters",command=clusters)
    button5.grid(row=8,column=4,padx=20,pady=10,sticky=NW)
    global button6
    def delclusters():
        global nodescolor2
        global G
        for node in nodescolor2.keys():
            G.nodes[node]['color'] = nodescolor2[node]
        nodescolor2={}
    button6=tk.Button(text="Remove clusters",command=delclusters)
    button6.grid(row=8,column=4,padx=20,pady=10,sticky=NE)
    global button7
    global entry7
    global label7
    entry7=tk.Entry(fenetre)
    entry7.grid(row=10,column=6,padx=20,pady=10,sticky=NE)
    def infonode():
        global G
        global label7
        x=int(entry7.get())
        if(label7!=None):
            label7.destroy()
        label7 = tk.Label(fenetre, text=nx.info(arg,n=x))
        label7.grid(row=11,column=6,padx=20,pady=10,sticky=NE)
    button7 = tk.Button(text='Info node', command=infonode)
    button7.grid(row=10,column=6,padx=20,pady=10,sticky=NW)
        
    
    

def destroyoptions(newplot):
    global canvas
    global toolbarFrame
    global button1
    global entry1
    global label1
    global button2
    global entry2
    global label2
    global button3
    global entry3
    global label3
    global button4
    global button5
    global button6
    global entry5
    if(canvas!=None):
        canvas.get_tk_widget().destroy()
    if(toolbarFrame!=None):
        toolbarFrame.destroy()
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
    if(button4!=None):
        button4.destroy()
    global buttonopt
    if(buttonopt!=None):
        buttonopt.destroy()
    if(button5!=None):
        button5.destroy()
    if(entry5!=None):
        entry5.destroy()
    if(button6!=None):
        button6.destroy()
    if(button7!=None):
        button7.destroy()
        label7.destroy()
        entry7.destroy()
    if(newplot==1):
        global listtodel
        while (listtodel!=[]):
            if(listtodel[0]!=None):
                listtodel[0].destroy()
            listtodel.pop(0)
  
def Validate(func,argList):
    global MajorData
    if(func==1):
        degmin=argList[0].get()
        widthmin=argList[1].get()
        starttime=argList[2].get()
        endtime=argList[3].get()
        paramk=argList[4].get()
        itera=argList[5].get()
        infec=argList[6].get()
        Networkx(MajorData,"Graph",degmin,widthmin,starttime,endtime,paramk,itera,infec,0)
      
    if(func==2):
        timestart=argList[0].get()
        timeend=argList[1].get()
        nbrmin=argList[2].get()
        sizeref=argList[3].get()
        Map(MajorData,"Map",timestart,timeend,nbrmin,sizeref,0)
        
    
    if(func==3):
        timestart=argList[0].get()
        timeend=argList[1].get()
        orange=argList[2].get()
        red=argList[3].get()
        BarChart(MajorData,"Interactions/id",timestart,timeend,orange,red,0)
        
    if(func==4):
        timestart=argList[0].get()
        timeend=argList[1].get()
        AdjacencyMatrix(MajorData,"AdjacencyMatrix",timestart,timeend,0)
        
    caract(0)


      
def ess(func,new):
    global listtodel
    global MajorData
    if(new==0):
        return
    if(func == 1):
        
        user_inputdeg = tk.IntVar(fenetre)
        user_inputwid = tk.IntVar(fenetre)
        user_inputtimS = tk.IntVar(fenetre) 
        user_inputtimE = tk.IntVar(fenetre)
        user_inputk = tk.DoubleVar(fenetre)
        user_inputite = tk.IntVar(fenetre)
        user_inputinf=tk.IntVar(fenetre)
        
        
        DeMin = Label(fenetre, text = "Minimal degree")
        DeMin.grid(row=12,column=1,sticky=W)
        Lam = Label(fenetre, text = "Minimal width")
        Lam.grid(row=13,column=1,sticky=W)
        TS = Label(fenetre, text = "Starting time")
        TS.grid(row=14,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time")
        TE.grid(row=15,column=1,sticky=W)
        kK = Label(fenetre, text = "K value")
        kK.grid(row=16,column=1,sticky=W)
        ITE = Label(fenetre, text = "Number of iter")
        ITE.grid(row=17,column=1,sticky=W)
        INF=Label(fenetre,text="Risky only?(0/1)")
        INF.grid(row=18,column=1,sticky=W)
        
        degmin = tk.Entry(fenetre, textvariable=user_inputdeg, width=8)
        degmin.grid(row = 12, column = 1, sticky=E)
        widthmin = tk.Entry(fenetre,textvariable=user_inputwid, width=8)
        widthmin.grid(row = 13, column = 1, sticky=E)
        timestart = tk.Entry(fenetre, textvariable=user_inputtimS, width=8)
        timestart.grid(row = 14, column = 1, sticky=E)
        timeend = tk.Entry(fenetre, textvariable=user_inputtimE, width=8)
        timeend.grid(row = 15, column = 1, sticky=E)
        k = tk.Entry(fenetre,textvariable=user_inputk, width=8)
        k.grid(row = 16, column = 1, sticky=E)
        ite = tk.Entry(fenetre,textvariable=user_inputite, width=8)
        ite.grid(row = 17, column = 1, sticky=E)
        inf = tk.Entry(fenetre,textvariable=user_inputinf,width=8)
        inf.grid(row=18,column=1,sticky=E)
        
        
        val = Button(fenetre, text='validate', command=lambda  arg1 = func , arg2=[user_inputdeg,user_inputwid,user_inputtimS,user_inputtimE, user_inputk,user_inputite,user_inputinf]: Validate(arg1,arg2))
        val.grid(row = 19, column = 1)
        
        listtodel.extend([DeMin,Lam,TS,TE,kK,ITE,degmin,widthmin,timestart,timeend,k,ite,val,INF,inf])
        
    if(func == 2):
        user_inputtimS = tk.IntVar(fenetre)
        user_inputtimE = tk.IntVar(fenetre)
        user_inputtimNbrm = tk.IntVar(fenetre)
        user_inputtimSizer = tk.IntVar(fenetre)
        
        TS = Label(fenetre, text = "Starting time")
        TS.grid(row=12,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time")
        TE.grid(row=13,column=1,sticky=W)
        NM = Label(fenetre, text = "Minimal number")
        NM.grid(row=14,column=1,sticky=W)
        SR = Label(fenetre, text = "Size of reference")
        SR.grid(row=15,column=1,sticky=W)
        
        timestart = tk.Entry(fenetre, textvariable=user_inputtimS, width=8)
        timestart.grid(row = 12, column = 1, sticky=E)
        timeend = tk.Entry(fenetre,textvariable=user_inputtimE, width=8)
        timeend.grid(row = 13, column = 1, sticky=E)
        nbrmin = tk.Entry(fenetre, textvariable=user_inputtimNbrm, width=8)
        nbrmin.grid(row = 14, column = 1, sticky=E)
        sizeref = tk.Entry(fenetre, textvariable=user_inputtimSizer, width=8)
        sizeref.grid(row = 15, column = 1, sticky=E)
        
        val = Button(fenetre, text='validate', command=lambda arg1 = func, arg2=[user_inputtimS,user_inputtimE,user_inputtimNbrm,user_inputtimSizer] : Validate(arg1,arg2))
        val.grid(row = 16, column = 1)
        
        listtodel.extend([TS,TE,NM,SR,timestart,timeend,nbrmin,sizeref,val])
    
    if(func == 3):
        user_inputtimMi = tk.IntVar(fenetre)
        user_inputtimMa = tk.IntVar(fenetre)
        user_inputOrange = tk.IntVar(fenetre)
        user_inputRed = tk.IntVar(fenetre)
        
        TS = Label(fenetre, text = "Starting time")
        TS.grid(row=12,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time")
        TE.grid(row=13,column=1,sticky=W)
        CO = Label(fenetre, text= "Orange limit")
        CO.grid(row=14,column=1,sticky=W)
        CR = Label(fenetre,text="Red limit")
        CR.grid(row=15,column=1,sticky=W)
        
        timestart = tk.Entry(fenetre, textvariable=user_inputtimMi, width=8)
        timestart.grid(row = 12, column = 1, sticky=E)
        timeend = tk.Entry(fenetre,textvariable=user_inputtimMa, width=8)
        timeend.grid(row = 13, column = 1, sticky=E)
        limorange=tk.Entry(fenetre,textvariable=user_inputOrange,width=8)
        limorange.grid(row = 14, column=1,sticky=E)
        limred = tk.Entry(fenetre,textvariable=user_inputRed,width=8)
        limred.grid(row=15,column=1,sticky=E)
        
        val = Button(fenetre, text='validate', command=lambda arg1=func, arg2=[user_inputtimMi,user_inputtimMa,user_inputOrange,user_inputRed] : Validate(arg1,arg2))
        val.grid(row = 16, column = 1)
        
        listtodel.extend([TS,TE,timestart,timeend,val,CO,CR,limred,limorange])
    
    if(func == 4):
        user_inputtimMi = tk.IntVar(fenetre)
        user_inputtimMa = tk.IntVar(fenetre)
        
        TS = Label(fenetre, text = "Starting time")
        TS.grid(row=12,column=1,sticky=W)
        TE = Label(fenetre, text = "Ending time")
        TE.grid(row=13,column=1,sticky=W)
        
        timestart = tk.Entry(fenetre, textvariable=user_inputtimMi, width=8)
        timestart.grid(row = 12, column = 1, sticky=E)
        timeend = tk.Entry(fenetre,textvariable=user_inputtimMa, width=8)
        timeend.grid(row = 13, column = 1, sticky=E)
        
        val = Button(fenetre, text='validate', command=lambda arg1=func,arg2=[user_inputtimMi,user_inputtimMa] : Validate(arg1,arg2))
        val.grid(row = 14, column = 1)

        listtodel.extend([TS,TE,timestart,timeend,val])
        
Separator(fenetre, orient=VERTICAL).grid(column=2, row=0, rowspan=40, sticky='ns')
ttk.Sizegrip()


buttonRead = Button(fenetre, text="Import Data from *.csv", command=ReadFile)
buttonRead.grid(row = 1, column = 1, sticky = W, columnspan = 1)

buttonClear = Button(fenetre, text="Clear Imported Data", command=ClearData).grid(row = 2, column = 1, sticky = W, columnspan = 1)
def showbuttons():
    boutonNextworkx=Button(fenetre, text="Graph (new window only)", command=lambda df=MajorData, title = "Graph", degmin=1,widthmin=1,timemin=0,timemax=timestepmax,k=0.1,iterations=50, infeconly=0,new=1 : Networkx(df,title,degmin,widthmin,timemin,timemax,k,iterations,infeconly,new)).grid(row = 3, column = 1, sticky = W, columnspan = 1)

    boutonInfection_Map=Button(fenetre, text="Interaction map", command=lambda df = MajorData, title = "Map of interactions" , timemin=0, timemax=50, nbremin=1, sizeref=10000,new=1: Map(df,title,timemin,timemax,nbremin,sizeref,new)).grid(row = 5, column = 1, sticky = W, columnspan = 1)

    boutonInteraction_people=Button(fenetre, text="Interaction/person", command=lambda df = MajorData, title = "Interaction/person" , timemin=0, timemax=timestepmax,orange=75,red=100,new=1: BarChart(df,title,timemin,timemax,orange,red,new)).grid(row = 4, column = 1, sticky = W, columnspan = 1)

    boutonAdjacency_Matrix=Button(fenetre, text="Adjacency matrix", command=lambda df = MajorData, title = "Adjacency matrix" ,timemin=0,timemax=timestepmax,new=1: AdjacencyMatrix(df,title,timemin,timemax,new)).grid(row = 6, column = 1, sticky = W, columnspan = 1)

    boutonInteraction_Number=Button(fenetre, text="Number of risky interactions", command=lambda df=MajorData, title = "Number of risky interactions" : Interplot(df, title)).grid(row = 7, column = 1, sticky = W, columnspan = 1)


    menubutton = Menubutton(fenetre, text="How to display the graph?")
    menubutton.grid(row = 9, column = 1, sticky = 'ew', columnspan = 1)

    menubutton.menu = Menu(menubutton, tearoff = 0, bg="red")
    menubutton["menu"] = menubutton.menu

    menubutton.menu.add_command(label="in the main window", command=lambda arg1 = "the main window": where(arg1))
    menubutton.menu.add_command(label="in another window", command=lambda arg1 = "another window": where(arg1))
    menubutton.menu.add_command(label="in the main window and in another window", command=lambda arg1 = "in the main window and in another window": where(arg1))
    menubutton.menu.add_command(label="remove the graphs of other windows", command=lambda arg1 = "remove the graphs": where(arg1))


def carac():
    boutonPlot_Caracteristics=Button(fenetre, text="Caracteristics of the plot ", command=lambda arg1=1: caract(arg1)).grid(row = 8, column = 1, sticky = W, columnspan = 1)





boutonExit=Button(fenetre, text="Close", command=ExitTotal).grid(row = 10, column = 1, sticky = W, columnspan = 1)



#fenetre.geometry('200x200')

col_count, row_count = fenetre.grid_size()
for col in range(col_count + 1):
    fenetre.grid_columnconfigure(col, minsize=40)
for row in range(row_count):
    fenetre.grid_rowconfigure(row, minsize=40)


def closeW():
    fenetre.close()

fenetre.geometry("750x600")
fenetre.mainloop()