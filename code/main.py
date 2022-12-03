import os
import time
import argparse
import networkx as nx
import sys
import heapq
from Approx import Approx
from LS1 import LS1_SA
from LS2 import Hill
from BnB import BNB

parser = argparse.ArgumentParser(description='Find Minimum Vertex Cover (MVC)')
parser.add_argument('-inst', help='Graph Instance')
parser.add_argument('-alg', help='Algorithm for finding the MVC')
parser.add_argument('-time', help='Cutoff Time (in secs)')
parser.add_argument('-seed', help='Random Seed')
args = parser.parse_args()

# Add the corresponding path for accessing the graph data files
data_path = './DATA/'
output_path= './output/'

def create_graph(file_name,VE=False):

    file_path = data_path + file_name
    graph_file = open(file_path, 'r')
    graph_data = graph_file.readlines()
    n_vertices, n_edges, is_weighted = graph_data[0].split()

    G = nx.Graph()

    for i, neighbours in enumerate(graph_data):
        if i != 0:
            neighbour = neighbours.split()
            for v in neighbour:
                G.add_edge(int(i), int(v))
                
    with open(file_path, 'r') as vertices:
        V, E, Temp = vertices.readline().split()
        return G, int(V), int(E), n_edges

if __name__=="__main__":

    G, V, E, num_edge = create_graph(args.inst)
    graph_file = args.inst
    cutoff = args.time
    randSeed = args.seed
    # print(G.edges(), G.nodes())

    if(args.alg == "BnB"):
        # Function call to the BnB Function
#         pass
        sol, trace = BNB(G, cutoff)

    elif(args.alg == "Approx"):
        # Function call to the Approx Function
        sol, trace = Approx(G)

    elif(args.alg == "LS1"):
        # Function call to the LS1 Function - Simulated Annealing
        sol, trace = LS1_SA(G,V,num_edge, cutoff, randSeed)
        
    elif(args.alg == "LS2"):
        # Function call to the LS2 Function
        sol, trace = Hill(G,V,E,randSeed,float(cutoff))

    else:
        print('-- Algo type missing --')
        exit()


    # Creating the solution and trace files for storing the data
    if(args.alg == "Approx" or args.alg=="BnB"):
        sol_file = output_path + graph_file[0:-6] + '_' + args.alg + '_' + cutoff + '.sol'
        trace_file = output_path + graph_file[0:-6] + '_' + args.alg + '_' + cutoff + '.trace'
    else:
        sol_file = output_path + graph_file[0:-6] + '_' + args.alg + '_' + cutoff + '_' + randSeed + '.sol'
        trace_file = output_path + graph_file[0:-6] + '_' + args.alg + '_' + cutoff + '_' + randSeed + '.trace'   

    f = open(sol_file, 'w')
    f.write(sol)
    f.close()

    f = open(trace_file, 'w')
    f.write(trace)
    f.close()
