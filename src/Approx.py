import time
import networkx as nx
import numpy as np

def Approx(G_,retVC=False):
    G = G_.copy()
    
    vertex_cover = []
    sol = ""
    trace = ""
    start = time.time()

    # Algo 4 - Edge Deletion
    # while G.number_of_edges() > 0:
    #     (u,v) = list(G.edges())[0]
        
    #     vertex_cover.append(u)
    #     vertex_cover.append(v)

    #     G.remove_node(u)
    #     G.remove_node(v)

        # print(G.number_of_edges(), G.number_of_nodes(), G.nodes())

    # Algo 1 - Maximum Degree Greedy (MDG)
    while G.number_of_edges() > 0:
        node_degree = [x[1] for x in G.degree]
        max_degree_node = list(G.degree)[np.argmax(node_degree)][0]

        vertex_cover.append(max_degree_node)
        G.remove_node(max_degree_node)

    # Algo 2 - Greedy Independent Cover
    # while G.number_of_edges() > 0:
    #     node_degree = [x[1] for x in G.degree]
    #     min_degree_node = list(G.degree)[np.argmin(node_degree)][0]    

    #     min_degree_node_neighbors = G.neighbors(min_degree_node)
    #     # print(G.degree, min_degree_node, min_degree_node_neighbors)
    #     G.remove_node(min_degree_node)

    #     for v in min_degree_node_neighbors:
    #         vertex_cover.append(v)
    #         G.remove_node(v)
    
    total_time = time.time() - start

    # Creating the solution and trace files

    vertex_cover.sort()
    sol += str(len(vertex_cover)) + '\n' + ','.join([str(v) for v in vertex_cover])
    trace += str(total_time) + ', ' + str(len(vertex_cover))
    if retVC:
        return sol, trace, vertex_cover
    else:
        return sol, trace
    # print(len(vertex_cover))
    # print(vertex_cover)
