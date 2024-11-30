import os
import collections

## We save the colour of each node in the dictionary dict_nodes, where each key is a node of the network and each 
## value is a list of the colour of the key node and an empty set. 

dict_nodes={}

with open ("./id_col.txt") as fp:
    for line in fp:
        line=line.split(" ")
        if int(line[1])==1:
            first_colour=set()
            dict_nodes[int(line[0])]=["colour_1", first_colour]
        elif int(line[1])==2:
            second_colour=set()
            dict_nodes[int(line[0])]=["colour_2", second_colour]
        else:
            third_colour=set()
            dict_nodes[int(line[0])]=["colour_3", third_colour]

## We collect in net all the edges in pairs of node ids.

net=[]

with open ("./edges_net.txt") as fp:
    for line in fp:
        line=line.split(" ")
        pair=[]
        pair.append(int(line[0]))
        pair.append(int(line[1]))
        net.append(pair)

for i in range (0, len(net)):
    current_sx=net[i][0]
    dict_nodes[current_sx][1].add(net[i][1])

for i in range (0, len(net)):
    current_dx=net[i][1]
    dict_nodes[current_dx][1].add(net[i][0])

for i in dict_nodes:
    transformed=list(dict_nodes[i][1])
    dict_nodes[i][1]=transformed

## We collect all the clusters with colour colour_1 in the list collection_cluster. 
## We also create the empty set visited_nodes to keep track of the visited nodes in the 
## process of exploring the network.

collection_cluster=[]
colour_cluster="colour_1"
visited_nodes=set()

## We explore the network. For each node in dict_nodes, we collect the maximal connected 
## subgraph with colour_1. We also flag the explored nodes while visiting the network.

for node in dict_nodes:
    
    if dict_nodes[node][0]==colour_cluster and node not in visited_nodes:
        
        visited_nodes.add(node)
        key_current_node=node
        current_cluster=[]
        current_node=dict_nodes[key_current_node]
        
        control_set=set()
        control_list=[]
        flag_set=set()

        current_cluster.append(key_current_node)
        flag_set.add(key_current_node)

        for i in range (0, len(current_node[1])):
            current=current_node[1][i]
            control_set.add(current)
            if dict_nodes[current][0]==current_node[0]:
                current_cluster.append(current)

        control_list=list(control_set)

        count=1

        while count > 0:
            control_list=list(control_set)
            for j in range (0, len(control_list)):
                current=control_list[j]
                if dict_nodes[current][0]==current_node[0]:
                    current_bis=dict_nodes[control_list[j]][1]
                    for q in range (0, len(current_bis)):
                        control_list.append(current_bis[q])
                        if dict_nodes[current_bis[q]][0]==current_node[0]:
                            current_cluster.append(current_bis[q])
                flag_set.add(control_list[j])

            control_set=set(control_list)           

            for j in flag_set:
                if j in control_set:
                    control_set.remove(j)

            count=len(control_set)

        for element in set(current_cluster):
            visited_nodes.add(element)
        current_cluster=list(set(current_cluster))
        collection_cluster.append(current_cluster)

collection_size=[]

for i in collection_cluster:
    current_size=len(i)
    collection_size.append(current_size)

## We count the internal edges, i.e. the edges_in of each cluster. 
## To do that, we check if the adjacent nodes show the same colour of the check_node.
## Then, we divide by 2, and we obtain the treelikeness as the ration betwe

collection_treel=[]

for q in range(0,len(collection_cluster)):
    current_cluster=collection_cluster[q]
   
    edges_in=0
    for i in range(0, len(current_cluster)):
        check_node=dict_nodes[current_cluster[i]]
        for j in range (0, len (check_node[1])):
            if dict_nodes[check_node[1][j]][0]==colour_cluster:
                edges_in=edges_in+1
    edges_in=edges_in/2
    
    if edges_in==0 or (len(current_cluster)-1)==0:
        treel=0.0
    else:
        treel=(len(current_cluster)-1)/edges_in
        
    collection_treel.append(treel)
