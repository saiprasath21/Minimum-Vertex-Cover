import os
import time
import argparse
import networkx as nx

parser = argparse.ArgumentParser(description='Find Minimum Vertex Cover (MVC)')
parser.add_argument('-inst', help='Graph Instance')
parser.add_argument('-alg', help='Algorithm for finding the MVC')
parser.add_argument('-time', help='Cutoff Time (in secs)')
parser.add_argument('-seed', help='Random Seed')
args = parser.parse_args()

def create_graph(cur_path, file_name):
    # data_path = cur_path + "\\data\\" + file_name

    # Add the corresponding path for accessing the graph data files
    data_path = 'C:\\Users\\Saiprasad\\Desktop\\Fall2022\\CSEA\\MVC\\data\\' + file_name

    graph_file = open(data_path, 'r')
    graph_data = graph_file.readlines()
    n_vertices, n_edges, is_weighted = graph_data[0].split()

    G = nx.Graph()

    for i, neighbours in enumerate(graph_data):
        if i != 0:
            neighbour = neighbours.split()
            for v in neighbour:
                G.add_edge(int(i), int(v))
    return G


if __name__=="__main__":
    cur_path = os.getcwd()
    G = create_graph(cur_path, args.inst)
    # print(G.edges(), G.nodes())

    if(args.alg == "BnB"):
        # Function call to the BnB Function
        pass

    elif(args.alg == "Approx"):
        # Function call to the Approx Function
        pass

    elif(args.alg == "LS1"):
        # Function call to the LS1 Function
        pass

    elif(args.alg == "LS2"):
        # Function call to the LS2 Function
        pass
    
    else:
        print('-- Algo type missing --')
        exit()

