## We save the adjacency of each node in the dictionary dict_adj, where each key is a node of the network and each 
## value is the list of nodes connected to the node in the key.

dict_adj=Dict()

for line in eachline("./edges_net.txt")
    new_line=rsplit(line, " ")
    new_line_vec = parse.(Int64,new_line)
    in_edge=new_line_vec[1]
    out_edge=new_line_vec[2]
    if haskey(dict_adj, in_edge)
        dict_adj[in_edge]= push!(dict_adj[in_edge],out_edge)  
    else
        dict_adj[in_edge]=Set()
        dict_adj[in_edge]= push!(dict_adj[in_edge],out_edge)    
    end
    if haskey(dict_adj, out_edge)
        dict_adj[out_edge]= push!(dict_adj[out_edge],in_edge)  
    else
        dict_adj[out_edge]=Set()
        dict_adj[out_edge]= push!(dict_adj[out_edge],in_edge)    
    end
end

for i in keys(dict_adj)
    dict_adj[i]=collect(dict_adj[i])
end

## We save the colour of each node in the dictionary dict_col, where each key is a node of the network and each 
## value is the colour of the node in the key. We also collect all the colours in the set colours.

dict_col=Dict()
colours=Set()

for line in eachline("./id_col.txt")
    new_line=rsplit(line, " ")
    new_line_vec = parse.(Int64,new_line)
    node=(new_line_vec[1])
    colour=(new_line_vec[2])
    colours=push!(colours,colour)
    dict_col[node]=colour
end

## We save the MFPT of each node to each of the colours available in the dictionary dict_hitting., where each key 
## is a node of the network, along with a value that is a list of the MFPT to all the available colours.
## Here, we initialise all the values of dict_hitting with lists of zero.

dict_hitting=Dict()

for i in keys(dict_col)
    dict_hitting[i]=[]
    for j = 1:length(colours)
        dict_hitting[i]=append!(dict_hitting[i], 0)
    end
end

## Here we define r_walkers as the number of random walks we want to run for evaluating MFPT starting from each node 
## of the net. 

r_walkers=1000
size_net=length(dict_col)

## Finally, we run the walks for all the q colours, collecting the MFPT in dict_hitting. Notice that we evaluate 
## MFPT from a node i to a node with colour q as the average over all the r_walkers. 

for i in keys(dict_col)
    for q in collect(colours)
        sum_walks_MFPT=0.0
        for j = 1:r_walkers
            hitting_target=q
            current_colour=""
            current_node=i
            while (current_colour!=hitting_target)
                node_choice=rand(dict_adj[current_node])
                sum_walks_MFPT=sum_walks_MFPT+1.0
                current_colour=dict_col[node_choice]
                current_node=node_choice
            end
        end
        average_walks_MFPT=sum_walks_MFPT/r_walkers
        dict_hitting[i][q+1]=average_walks_MFPT

    end
end

