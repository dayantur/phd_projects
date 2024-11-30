import os
import collections
import random

## We save the adjacency of each node in the dictionary dict_adj, where each key is a node of the network and each 
## value is the list of nodes connected to the node in the key.

dict_adj={}

with open ("./edges_net.txt") as fp:
    for line in fp:
        line=line.split(" ")
        in_edge=int(line[0])
        out_edge=int(line[1])
        if in_edge in dict_adj:
            dict_adj[in_edge].add(out_edge)
        else:
            dict_adj[in_edge]=set()
            dict_adj[in_edge].add(out_edge)
            
        if out_edge in dict_adj:
            dict_adj[out_edge].add(in_edge)
        else:
            dict_adj[out_edge]=set()
            dict_adj[out_edge].add(in_edge)

for i in dict_adj:
    dict_adj[i]=list(dict_adj[i])

## We save the colour of each node in the dictionary dict_col, where each key is a node of the network and each 
## value is the colour of the node in the key. We also collect all the colours in the set colours.


dict_col={}
colours=set()

with open ("./id_col.txt") as fp:
    for line in fp:
        line=line.split(" ")
        node=int(line[0])
        colour=int(line[1])
        colours.add(colour)
        dict_col[node]=colour

dict_col_restricted={}

for i in dict_col:
    if dict_col[i]==1 or dict_col[i]==2:
        dict_col_restricted[i]=dict_col[i]

all_col=[]

for i in dict_col_restricted:
    all_col.append(dict_col_restricted[i])

all_col_r = random.sample(all_col, len(all_col))

dict_resh={}
count=0

for i in dict_col_restricted:
    dict_resh[i]=all_col_r[count]
    count=count+1

dict_final={}
for i in dict_col:
    if i in dict_resh:
        dict_final[i]=dict_resh[i]
    else:
        dict_final[i]=dict_col[i]

