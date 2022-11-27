import time
import networkx as nx
import numpy as np

def Approx(G_):
    G = G_.copy()
    
    vertex_cover = []

    # Algo 4 - Edge Deletion
    while G.number_of_edges() > 0:
        (u,v) = list(G.edges())[0]
        
        vertex_cover.append(u)
        vertex_cover.append(v)

        G.remove_node(u)
        G.remove_node(v)

        # print(G.number_of_edges(), G.number_of_nodes(), G.nodes())

    # Algo 1 - Maximum Degree Greedy (MDG)
    while G.number_of_edges() > 0:
        node_degree = [x[1] for x in G.degree]
        max_degree_node = list(G.degree)[np.argmax(node_degree)][0]

        vertex_cover.append(max_degree_node)
        G.remove_node(max_degree_node)

    # Algo 2 - Greedy Independent Cover
    while G.number_of_edges() > 0:
        node_degree = [x[1] for x in G.degree]
        min_degree_node = list(G.degree)[np.argmin(node_degree)][0]    

        min_degree_node_neighbors = G.neighbors(min_degree_node)
        # print(G.degree, min_degree_node, min_degree_node_neighbors)
        G.remove_node(min_degree_node)

        for v in min_degree_node_neighbors:
            vertex_cover.append(v)
            G.remove_node(v)
    
    print(vertex_cover)
