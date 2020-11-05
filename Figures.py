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


"""
class node:
    def __init__(self):
        self._x=random.random()*1
        self._y=random.random()*1 
        self._force_x=0
        self._force_y=0
"""    
def main():
    #plt.ion()
    df = pandas.read_csv('Small_dataset.csv',sep=r'\s*,\s*')
    nodes=ForceLayout(df,50,5000,1,0.004,10000)
    G,colors=GraphG(df,nodes)
    ForceGraph(df,nodes,G,colors)
    Networkx(df,nodes,G,colors)
    Hover(df,G)
    #Netgraph(df,nodes,G)
    Map(df)
    AdjacencyMatrix(df)
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
   
    for a in range(10000): 
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
"""
for i in range(N):
    print(nodes[i].x, nodes[i].y)
    print(nodes[i].force_x, nodes[i].force_y)
    print("\n")
    plt.plot(nodes[i].x,nodes[i].y, 'o',color='black')    
"""
def GraphG(df,nodes):
    M=len(df['person1'])
    G=nx.Graph()
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    for i in range(N):
        G.add_node(i)
    for i in range(M):
        if(df['infected1'][i]!=df['infected2'][i]):
            G.add_edge(df['person1'][i],df['person2'][i],color='red')
        else:
            G.add_edge(df['person1'][i],df['person2'][i],color='black')
        

    colors = [G[u][v]['color'] for u,v in G.edges()]  
    return G,colors

#GRAPH Force-Layout
def ForceGraph(df,nodes,G,colors):
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    for i in range(N):
        G.nodes[i]['pos']=(nodes[i][0],nodes[i][1])

    plt.figure()    
    plt.title("Graph of interactions with force layout")
    nx.draw(G,pos=nx.get_node_attributes(G, 'pos'),with_labels=True,font_weight='bold',edge_color=colors, width=2.5)

#GRAPH Networkx
def Networkx(df,nodes,G,colors):
    
    plt.figure()
    plt.title("Graph of interactions with networkx algorithm")
    nx.draw(G,with_labels=True,font_weight='bold',edge_color=colors, width=2.5)
    
#Bokeh    
def Hover(df,G):
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    homeok=[0]*N
    M=len(df['person1'])
    for i in range(M):
        if(homeok[df['person1'][i]]==0):
            G.nodes[df['person1'][i]]['home']=(df['home1_long'][i],df['home1_lat'][i])
            homeok[df['person1'][i]]=1
        if(homeok[df['person2'][i]]==0):
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
def Map(df):
    M=len(df['person1'])
    long_min=(df['loc_long'].min())
    long_max=(df['loc_long'].max())
    lat_min=(df['loc_lat'].min())
    lat_max=(df['loc_lat'].max())
    long_dif=(long_max-long_min)/4
    lat_dif=(lat_max-lat_min)/4
    BBox=(long_min-long_dif, long_max+long_dif,lat_min-lat_dif,lat_max+lat_dif)

    map_m = plt.imread('map.png')
    plt.figure()
    deja=[0]*M
    for i in range(M):
        if deja[i]==0:
            count=1
            for j in range(i+1,M):
                if((df['loc_long'][i]==df['loc_long'][j]) and (df['loc_lat'][i]==df['loc_lat'][j])):
                    count=count+1
                    deja[j]=1
            plt.scatter(df['loc_long'][i], df['loc_lat'][i], zorder=1, alpha= 1, c='black', s=100*count)            
  
    plt.title('Infection map')
    plt.xlim(BBox[0],BBox[1])
    plt.ylim(BBox[2],BBox[3])
    plt.imshow(map_m, zorder=0, extent=BBox, aspect=2)

#Adjacency Matrix
def AdjacencyMatrix(df):
    M=len(df['person1'])
    N1=df['person1'].max()
    N2=df['person2'].max()
    N=max(N1,N2)+1
    data=np.zeros((N,N))
    for i in range(M):
        p1=df['person1'][i]
        p2=df['person2'][i]
        data[p1][p2]=(data[p1][p2])+1
        data[p2][p1]=(data[p2][p1])+1
    az=sns.clustermap(data,cmap="YlGnBu")
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

def c():
    plt.close('all')
    

    