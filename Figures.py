import numpy as np
import matplotlib.pyplot as plt
import math
import pandas
import random
import networkx as nx
import seaborn as sns 


MAX_DISPLACEMENT_SQUARED = 10000

df = pandas.read_csv('Small_dataset.csv',sep=r'\s*,\s*')

L = 50 #spring rest length
K_r = 2000 #repulsive force constant
K_s = 1  #spring constant
delta_t = 0.004 # time step

class node:
      x=random.random()*1
      y=random.random()*1
      force_x=0
      force_y=0   

T=df['timestep'].max()+1
M=len(df['person1'])
N1=df['person1'].max()
N2=df['person2'].max()
N=max(N1,N2)+1
nodes=[0]*N 
for i in range(N):
    nodes[i]=node()

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
            dx = node2.x - node1.x
            dy = node2.y - node1.y
            if (dx != 0 or dy != 0):
                distanceSquared = dx*dx + dy*dy
                distance = math.sqrt( distanceSquared )
                force = K_r / distanceSquared
                fx = force * dx / distance
                fy = force * dy / distance
                node1.force_x = node1.force_x - fx
                node1.force_y = node1.force_y - fy
                node2.force_x = node2.force_x + fx
                node2.force_y = node2.force_y + fy
            else:
              node1.force_x = node1.force_x - random.random()
              node1.force_y = node1.force_y - random.random()
              node2.force_x = node2.force_x + random.random()
              node2.force_y = node2.force_y + random.random()
    # spring force between adjacent pairs
    for i1 in range(N):
        node1 = nodes[i1]
        for i2 in neighbors[i1]:
            node2 = nodes[i2]
            if i1 < i2:
                dx = node2.x - node1.x
                dy = node2.y - node1.y
                if (dx != 0 or dy != 0):
                    distance = math.sqrt( dx*dx + dy*dy )
                    force = K_s * ( distance - L )
                    fx = force * dx / distance
                    fy = force * dy / distance
                    node1.force_x = node1.force_x + fx
                    node1.force_y = node1.force_y + fy
                    node2.force_x = node2.force_x - fx
                    node2.force_y = node2.force_y - fy
                            
    # update positions
    for i in range(N):
        node = nodes[i]
        dx = delta_t * node.force_x
        dy = delta_t * node.force_y
        displacementSquared = dx*dx + dy*dy
        if (displacementSquared>MAX_DISPLACEMENT_SQUARED):
            s = math.sqrt( MAX_DISPLACEMENT_SQUARED / displacementSquared )
            dx = dx * s
            dy = dy * s
        node.x = node.x + dx
        node.y = node.y + dy
            
#PLOT    
"""
for i in range(N):
    print(nodes[i].x, nodes[i].y)
    print(nodes[i].force_x, nodes[i].force_y)
    print("\n")
    plt.plot(nodes[i].x,nodes[i].y, 'o',color='black')    
"""
#GRAPH Force-Layout
G=nx.Graph()
for i in range(N):
    G.add_node(i)
    G.nodes[i]['pos']=(nodes[i].x,nodes[i].y)
for i in range(len(df['person1'])):
    if(df['infected1'][i]!=df['infected2'][i]):
        G.add_edge(df['person1'][i],df['person2'][i],color='red')
    else:
        G.add_edge(df['person1'][i],df['person2'][i],color='black')

colors = [G[u][v]['color'] for u,v in G.edges()]     

plt.figure()
plt.title("Graph of interactions with force layout")
nx.draw(G,pos=nx.get_node_attributes(G, 'pos'),with_labels=True,font_weight='bold',edge_color=colors, width=2.5)


#GRAPH Networkx

plt.figure()
plt.title("Graph of interactions with networkx algorithm")
nx.draw(G,with_labels=True,font_weight='bold',edge_color=colors, width=2.5)

#MAP

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
data=np.zeros((N,N))
for i in range(M):
    p1=df['person1'][i]
    p2=df['person2'][i]
    data[p1][p2]=(data[p1][p2])+1
    data[p2][p1]=(data[p2][p1])+1
az=sns.clustermap(data,cmap="YlGnBu")
az.fig.suptitle('Adjacency matrix') 

#Risky interactions plot

TimeI = [0]*T
for i in range(M):
    if(df['infected1'][i]!=df['infected2'][i]):
        TimeI[df['timestep'][i]]=(TimeI[df['timestep'][i]])+1
plt.figure()
plt.title("Risky interactions")
plt.plot(TimeI)

#Bar-chart of number of interactions

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
    

    
