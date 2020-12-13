import numpy as np
import matplotlib.pyplot as plt;
import math
import pandas
import random
import networkx as nx
import seaborn as sns 
import netgraph
from bokeh.io import show
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool,PointDrawTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4
from grave import plot_network
from grave.style import use_attributes
from matplotlib.colors import LogNorm
from matplotlib.colors import LinearSegmentedColormap

"""
class node:
    def __init__(self):
        self._x=random.random()*1
        self._y=random.random()*1 
        self._force_x=0
        self._force_y=0
"""   
textvar= None 
def main():
    #plt.ion()
    c()
    df = pandas.read_csv('scenario1.csv',sep=r'\s*,\s*')
    timestepmax=df['timestep'][len(df['timestep'])-1]
    #nodes=ForceLayout(df,50,10000,1,0.004,10000)
    G=GraphG(df,1,2,0,20)
    #ForceGraph(df,nodes,G,colors,weigths,NN)
    Networkx(df,G) 
    #Hover(df,G,NN)
    #Netgraph(df,nodes,G)
    Map(df,0,50,1,10000)
    AdjacencyMatrix(df,0,timestepmax)
    Interplot(df)
    BarChart(df)
    

def ForceLayout(df,L,K_r,K_s,delta_t,MAX_DISPLACEMENT_SQUARED):
    """
    L = 50 #spring rest length
    K_r = 3000 #repulsive force constant
    K_s = 1  #spring constant
    delta_t = 0.004 # time step
    MAX_DISPLACEMENT_SQUARED = 10000
    """  
   
    M=len(df['person1'])
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    nodes=np.zeros((N,4)) 
    for i in range(N):
        nodes[i][0]=random.random()*1000
        nodes[i][1]=random.random()*1000

    
    neighbors = [set() for _ in range(N)]  
        
    for i in range(M):
        neighbors[df['person1'][i]].add(df['person2'][i])
        neighbors[df['person2'][i]].add(df['person1'][i])
   
    for a in range(1000): 
        # repulsion between all pairs
        for i1 in range(N-1):
            node1 = nodes[i1]
            for i2 in range (i1+1,N):
                node2 = nodes[i2]
                dx = node2[0] - node1[0]
                dy = node2[1] - node1[1]
                if (dx != 0 or dy != 0):
                    distanceSquared = dx*dx + dy*dy
                    distance = math.sqrt( distanceSquared )
                    force = K_r / distanceSquared
                    fx = force * dx / distance
                    fy = force * dy / distance
                    node1[2] = node1[2] - fx
                    node1[3] = node1[3] - fy
                    node2[2] = node2[2] + fx
                    node2[3] = node2[3] + fy
                else:
                    node1[2] = node1[2] - random.random()
                    node1[3] = node1[3] - random.random()
                    node2[2] = node2[2] + random.random()
                    node2[3] = node2[3] + random.random()
        # spring force between adjacent pairs
        for i1 in range(N):
            node1 = nodes[i1]
            for i2 in neighbors[i1]:
               node2 = nodes[i2]
               if i1 < i2:
                   dx = node2[0] - node1[0]
                   dy = node2[1] - node1[1]
                   if (dx != 0 or dy != 0):
                       distance = math.sqrt( dx*dx + dy*dy )
                       force = K_s * ( distance - L )
                       fx = force * dx / distance
                       fy = force * dy / distance
                       node1[2] = node1[2] + fx
                       node1[3] = node1[3] + fy
                       node2[2] = node2[2] - fx
                       node2[3] = node2[3] - fy
                            
        # update positions
        for i in range(N):
            node = nodes[i]
            dx = delta_t * node[2]
            dy = delta_t * node[3]
            displacementSquared = dx*dx + dy*dy
            if (displacementSquared>MAX_DISPLACEMENT_SQUARED):
                s = math.sqrt( MAX_DISPLACEMENT_SQUARED / displacementSquared )
                dx = dx * s
                dy = dy * s
            node[0] = node[0] + dx
            node[1] = node[1] + dy
    return nodes 

       
#PLOT 
def GraphG(df,degmin,widthmin,timestart,timeend):
    M=len(df['person1'])
    G=nx.Graph()
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    intdict={}
    for i in range(N):
        G.add_node(i,size=50,homelong=0,homelat=0)
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
        if(value[0]>widthmin):
            if(value[1]==1):
                G.add_edge(key[0],key[1],color='red',width=min((value[0]/5),7))
            else:
                G.add_edge(key[0],key[1],color='black',width=min((value[0]/5),7))
    for i in range(M):
        G.nodes[df['person1'][i]]['homelong']=df['home1_long'][i]
        G.nodes[df['person1'][i]]['homelat']=df['home1_lat'][i]
        G.nodes[df['person2'][i]]['homelong']=df['home2_long'][i]
        G.nodes[df['person2'][i]]['homelat']=df['home2_lat'][i]
    for i in range(N):
        if(G.degree(i)<degmin):
            G.remove_node(i)
    d=dict(G.degree)
    for k in d.keys():
        G.nodes[k]['size'] = 20+10*d[k]
    return G

#GRAPH Force-Layout
def ForceGraph(df,nodes,G,colors,weights,NN):
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    for i in range(N):
        if(NN[i]==1):
            G.nodes[i]['pos']=(nodes[i][0],nodes[i][1])

    plt.figure()    
    plt.title("Graph of interactions with force layout")
    nx.draw(G,pos=nx.get_node_attributes(G, 'pos'),with_labels=True,font_weight='bold',edge_color=colors, width=weights)


#GRAPH Networkx
def Networkx(df,G):
    def spring_layout(networkx):
        """
        Let's build my own layout. It's going to be random, except for a handful
        of points!
        """
        pos = nx.spring_layout(G,k=0.07,iterations=50)
        return pos
  
    plt.ion()
    fig, ax = plt.subplots()
    plt.title("Graph of interactions with networkx algorithm")
    #nx.draw(G,with_labels=True,font_weight='bold',edge_color=colors, width=weigths)
    art = plot_network(G, layout=spring_layout, ax=ax,node_style=use_attributes(), edge_style=use_attributes())
    art.set_picker(10)
    fig.canvas.mpl_connect('pick_event', hilighter)
    
#Bokeh    
def Hover(df,G,NN):
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    homeok=[0]*N
    M=len(df['person1'])
    for i in range(M):
        if((NN[df['person1'][i]]==1)and(homeok[df['person1'][i]]==0)):
            G.nodes[df['person1'][i]]['home']=(df['home1_long'][i],df['home1_lat'][i])
            homeok[df['person1'][i]]=1
        if((NN[df['person2'][i]]==1)and(homeok[df['person2'][i]]==0)):
            G.nodes[df['person2'][i]]['home']=(df['home2_long'][i],df['home2_lat'][i])
            homeok[df['person2'][i]]=1
        
    plot = Plot(plot_width=400, plot_height=400,x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Graph Interaction Demonstration"
    node_hover_tool = HoverTool(tooltips=[("home", "@home")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
    plot.add_tools(PointDrawTool(renderers = [graph_renderer.node_renderer], empty_value = 'black'))
    plot.renderers.append(graph_renderer)
    
    show(plot)

#Graph netgraph
def Netgraph(df,nodes,G):
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    
    labeldict={}
    for i in range(N):
        labeldict[i]=i
    maxx=0
    maxy=0
    for  i in range(N):
        if nodes[i][0]>maxx:
            maxx=nodes[i][0]
        if nodes[i][1]>maxy:
            maxy=nodes[i][1]
    posdict={}
    for i in range(N):
        posdict[i]=(nodes[i][0]/(3*maxx),nodes[i][1]/(3*maxy))
    plt.figure()
    plt.ion()
    plt.title("Interactive netGraph of interactions with force layout")
    plt_ins=netgraph.InteractiveGraph(G,node_positions=posdict,node_labels=labeldict)

#MAP
def Map(df,timestart,timeend,nbrmin,sizeref):
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
    plt.figure()
    for i in range(start,end):
        x= df['loc_long'][i]
        y= df['loc_lat'][i]
        if (x,y) in locdict.keys():
            locdict[(x,y)]=locdict[(x,y)]+1
        else:
            locdict[(x,y)]=1
                
    """  if deja[i]==0:
            count=1
            for j in range(i+1,end):
                if((df['loc_long'][i]==df['loc_long'][j]) and (==df['loc_lat'][j])):
                    count=count+1
                    deja[j]=1
        size=sizeref*count/ntot """
    for key,value in locdict.items():
        if(value>=nbrmin) :    
            plt.scatter(key[0], key[1], zorder=1, alpha= 1, c='black', s=value*sizeref/ntot)  
  
    plt.title('Interaction map')
    plt.xlim(BBox[0],BBox[1])
    plt.ylim(BBox[2],BBox[3])
    plt.imshow(map_m, zorder=0, extent=BBox, aspect=2)

#Adjacency Matrix
def AdjacencyMatrix(df,timemin,timemax):
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
        mask=(data==0)
  )
    az.fig.suptitle('Adjacency matrix') 

#Risky interactions plot
def Interplot(df):
    M=len(df['person1'])
    T=df['timestep'].max()+1
    TimeI = [0]*T
    for i in range(M):
        if(df['infected1'][i]!=df['infected2'][i]):
            TimeI[df['timestep'][i]]=(TimeI[df['timestep'][i]])+1
    plt.figure()
    plt.title("Risky interactions")
    plt.plot(TimeI)

#Bar-chart of number of interactions
def BarChart(df):
    M=len(df['person1'])
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    nbinter=[0]*N
    for i in range(M):
        nbinter[df['person1'][i]]=nbinter[df['person1'][i]]+1
        nbinter[df['person2'][i]]=nbinter[df['person2'][i]]+1
        index= sorted(range(N), key=lambda k: nbinter[k],reverse=True)
        nbinter=sorted(nbinter,reverse=True)

    plt.figure()
    plt.title("Number of interactions")
    for i in range(N):
        plt.bar(str(index[i]),nbinter[i], align='center',color='blue')   

def hilighter(event):
    # if we did not hit a node, bail
    if not hasattr(event, 'nodes') or not event.nodes:
        return

    # pull out the graph,
    graph = event.artist.graph

    # clear any non-default color on nodes
    for node, attributes in graph.nodes.data():
        attributes.pop('color', None)

    #for u, v, attributes in graph.edges.data():
      #  attributes.pop('width', None)

    for node in event.nodes:
        graph.nodes[node]['color'] = 'C1'

    #for edge_attribute in graph[node].values():
      #   edge_attribute['width'] = 3
         
    for node in event.nodes:
        global textvar
        if(textvar!=None):
            textvar.remove()
        textvar=plt.text(1,1,'Home localisation \nid=%d \nlong=%f \nlat=%f' %(node,graph.nodes[node]['homelong'],graph.nodes[node]['homelat']),bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        
    # update the screen
    event.artist.stale = True
    event.artist.figure.canvas.draw_idle()
       
    
def c():
    plt.close('all')
    
main()
    

    