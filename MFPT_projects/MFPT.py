import random
import os
import collections

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

## We save the MFPT of each node to each of the colours available in the dictionary dict_hitting., where each key 
## is a node of the network, along with a value that is a list of the MFPT to all the available colours.
## Here, we initialise all the values of dict_hitting with lists of zero.

dict_hitting={}

for i in dict_col:
    dict_hitting[i]=[]
    for j in range(0,len(colours)):
        dict_hitting[i].append(0)

## Here we define r_walkers as the number of random walks we want to run for evaluating MFPT starting from each node 
## of the net. 

r_walkers=10000
size_net=len(dict_col)

## Finally, we run the walks for all the q colours, collecting the MFPT in dict_hitting. Notice that we evaluate 
## MFPT from a node i to a node with colour q as the average over all the r_walkers. 

for i in dict_col:
    for q in list(colours):
        sum_walks_MFPT=0.0
        for j in range (0, r_walkers):
            hitting_target=q
            current_colour=""
            current_node=i
            while (current_colour!=hitting_target):
                node_choice=random.choice(dict_adj[current_node])
                sum_walks_MFPT=sum_walks_MFPT+1.0
                current_colour=dict_col[node_choice]
                current_node=node_choice
        average_walks_MFPT=sum_walks_MFPT/float(r_walkers)
        dict_hitting[i][q]=average_walks_MFPT