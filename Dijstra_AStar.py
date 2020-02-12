# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:53:53 2018

@author: KUSHAL
"""
input_files = ['input_1.txt', 'input_2.txt' , 'input_3.txt']
coords_files = ['coords_1.txt','coords_2.txt','coords_3.txt']

def main(input_file, coord_file, heur_weight):
    
    try:
        
        import numpy as np
        import math as mt
    except:
        print ('Install numpy and math')
    
#    try:
#        import networkx as nx
#        import matplotlib.pyplot as plt
#    except:
#        pass
    # =============================================================================
    # Defining the function for sorting data from the input files and storing it in a nested list
    # =============================================================================
    
    def sort_data(input_file):        
        """This function sorts the data from the input file into a list"""                  
        with open(input_file,"r") as input_file:        #open file
            data = input_file.readlines()               #read lines from the text file
            row_data = []                               #initiate a multidimensional list to store the data
            for line in data:                           #split the words in each line and store them in row_data
                row_data.append(line.split()) 
            row_float = []
            for thing in row_data:
                row_float.append(list(map(float,thing)))
            return row_float                              #return the list in float
    
    # =============================================================================
    # Assigning the variables with number of vertices and specifying
    # the start and the end vertex       
    # Reading the coordinates and storing the list of coordinates for the given points
    # =============================================================================
    
    input_vertices = sort_data(input_file)
    Coordinates = sort_data(coord_file)
    
    vertice_count = int(input_vertices[0][0])
    start_vertex = int(input_vertices[1][0])
    end_vertex = int(input_vertices[2][0])
    
    del input_vertices[0:3]
    input_vertices = np.array(input_vertices)    # input_vertices is a numpy array showing the graph
    
    
    
    # =============================================================================
    # Computing the cost array which stores the cost of going from one vertex to
    # its adjacent vertices
    # =============================================================================
    
    cost_array = np.zeros((int(max(input_vertices[:,0])+1),int(max(input_vertices[:,1])+1)))
    
    cost_array = np.full_like(cost_array, np.inf)
    
    for i in range(len(input_vertices[:,0])):
        cost_array[int(input_vertices[i,0]),int(input_vertices[i,1])] = input_vertices[i,2]
    
    
    
    # =============================================================================
    # Defining Heuristics Function
    # =============================================================================
    def heuristic(point,end_vertex):
        euclidian_distance = mt.sqrt((Coordinates[point][0] - Coordinates[end_vertex][0])**2 + (Coordinates[point][1] - Coordinates[end_vertex][1])**2)
        return euclidian_distance
    
    
    # =============================================================================
    # Implementing the Dijkstra/A* algorithm
    # =============================================================================
    
    
    Open_list = [start_vertex]
    Closed_list = []
    V = np.zeros((int(vertice_count+1)))
    V = np.full_like(V, np.inf)
    V[start_vertex] = 0
    B = np.zeros((int(vertice_count+1)))
    
    def find_neighbors(vertice):
        """This function finds the neighbours of the vertex specified as vertice"""
        neighbors = []
        delta = 0
        for kau in range(1,int(max(input_vertices[:,1]))):
            if cost_array[vertice,kau] != np.inf and cost_array[vertice,kau] != 0:
                delta +=1
                neighbors.append(kau)
        return neighbors, delta
    
    
    count = 0
    
    while end_vertex not in Closed_list: 
        curr_cost = []
        for kes in Open_list:
            curr_cost.append(V[kes] + heur_weight * heuristic(kes,end_vertex))
        min_cost_open_handle = np.argmin(curr_cost)
        min_cost_open = Open_list[min_cost_open_handle]
        del curr_cost[min_cost_open_handle]     
        [neighbors,delta] = find_neighbors(min_cost_open)       
        Open_list.remove(min_cost_open)         
        Closed_list.append(min_cost_open)
        count += 1
        for neigh in neighbors:
            if neigh not in Closed_list and neigh not in Open_list:
                Open_list.append(neigh)
            if neigh not in Closed_list:
                Vnew = cost_array[min_cost_open,neigh] + V[min_cost_open]
                if Vnew < V[neigh]:
                    V[neigh] = Vnew
                    B[neigh] = min_cost_open
    
    
    V_opt = V[end_vertex]
    
    
    path = []
    path.append(end_vertex)
    i = int(end_vertex)
    while start_vertex not in path:
        path.append(int(B[i]))
        i = int(B[i])
    
    
    del i 
    Pos = {}
    X = nx.DiGraph()
    for i in range(1,int(vertice_count)+1):    
        Pos.update({i:(Coordinates[i-1][0],Coordinates[i-1][1])})
    
    
    vertices_tuple = [tuple(row) for row in input_vertices]
    X.add_nodes_from(Pos.keys())
    
    #XY=nx.shortest_path(X,6,94) 
    
    attrs = {20: {'size' : 2}}
    nx.set_node_attributes(X,attrs)
    X.add_weighted_edges_from(vertices_tuple)
    
    nx.draw_networkx(X, Pos,font_size = 3, node_size = 15, arrows = False)
    
    nx.draw_networkx_nodes(X, Pos, nodelist = Closed_list, node_size = 20, node_color = 'y')
    nx.draw_networkx_nodes(X, Pos, nodelist = Open_list , node_color = 'g', node_size = 20)
    nx.draw_networkx_nodes(X, Pos, nodelist = [start_vertex], node_color = 'b', node_size=20)
    nx.draw_networkx_nodes(X, Pos, nodelist = [end_vertex], node_color = 'b', node_size = 20)
    nx.draw_networkx_nodes(X, Pos, nodelist = path , node_color = 'c', node_size = 30)
    figure = plt.figure(figsize=(8,8))
    
    plt.axis("off")
    figure.savefig(input_file+'.png', dpi = 700)
    plt.clf()
    
    return V_opt , count, path


with open('output_costs.txt', 'w') as file_costs, open('output_numiters.txt', 'w') as file_numiters:    
    for i in range(len(input_files)):
        for j in [0,1]:
            [V_Op,iterations, path] =  main(input_files[i],coords_files[i],j)
            file_costs.write('%0.6f ' %V_Op)
            file_numiters.write('%d ' %iterations)
        file_costs.write('\n')
        file_numiters.write('\n')
        
#        print('file:'+ input_files[i])    
#        print('Optimum cost: ' + str(V_Op))
#        print('Number of iterations: ' + str(iterations))
#        print('===========================')

