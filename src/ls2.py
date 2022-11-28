import time
import random
import networkx as nx
import numpy as np

def initial_solution(G, start_time, cutoff, trace_output):
		temp_G = G.nodes()
		VC = sorted(list(zip(list(G.degree(temp_G).values()), temp_G)))
		VC_sol = temp_G
		i=0
		uncov_edges=[]
		optvc_len = len(VC_sol)
		while(i < len(VC) and (time.time() - start_time) < cutoff):
			flag=True
			for x in G.neighbors(VC[i][1]):
				if x not in temp_G:
					flag = False
			if flag:	
				temp_G.remove(VC[i][1])
			i=i+1
		print('Heurestic Solution:' + str(len(VC_sol)))
		return VC_sol, trace_output	

# Helper method to add a vertex
def addV(G, VertCover, conf_check, dscores, edge_weights, uncov_edges, add):
    dscores[add] = -dscores[add]
    for x in G.neighbors(add):
        if x not in VertCover:
            uncov_edges.remove((add,x))
            uncov_edges.remove((x,add))
            conf_check[x] = 1
            dscores[x] -= edge_weights[add][x]
        else:
            dscores[x] += edge_weights[add][x]

# Helper method to remove a vertex
def removeV(G, VertCover, conf_check, dscores, edge_weights, uncov_edges, removed):
    dscores[removed] = -dscores[removed]
    conf_check[removed] = 0
    for x in G.neighbors(removed):
        if x not in VertCover:
            uncov_edges.append((removed,x))
            uncov_edges.append((x,removed))
            conf_check[x] = 1
            dscores[x] += edge_weights[removed][x]
        else:
            dscores[x] -= edge_weights[removed][x]


def Hill(G, V, E, randSeed,cutoff):
    # Initialization
    trace_output=[]

    VertCover, trace_output = initial_solution(G, start_time, cutoff, trace_output)

    vertex_cover = []
    sol = ""
    trace = ""

    random.seed(randSeed)

    threshold = .5*V
    reduction_factor = .3

    edge_weights = nx.convert.to_dict_of_dicts(G, edge_data=1)

    conf_check = [1]*(V+1)
    dscores = [0]*(V+1)
    uncov_edges=[]

    VC_sol = VertCover.copy()
    optvc_len = len(VertCover)
    avg_weight = 0
    delta_weight = 0

    start_time = time.time()

    #HillClimb Implementation

    while((time.time() - start_time) < cutoff):	

        # If it is a vertex cover: remove the max cost node		
        while not uncov_edges:
            if (optvc_len > len(VertCover)):
                trace_output.append((optvc_len,time.time()-start_time))					
                VC_sol = VertCover.copy()	
                optvc_len = len(VertCover)
            max_improv = -float('inf')
            for x in VertCover:
                if dscores[x] > max_improv:
                    max_improv = dscores[x]
                    opt_rem = x
            VertCover.remove(opt_rem)
            removeV(G, VertCover, conf_check, dscores, edge_weights, uncov_edges, opt_rem)


        # remove max cost node from solution
        max_improv = -float('inf')
        for x in VertCover:
            if dscores[x] > max_improv:
                max_improv = dscores[x]
                opt_rem = x
        VertCover.remove(opt_rem)
        removeV(G, VertCover, conf_check, dscores, edge_weights, uncov_edges, opt_rem)



        # find node from random uncovered edge to add
        randEdge = random.choice(uncov_edges)
        if conf_check[randEdge[0]] == 0 and randEdge[1] not in VertCover: 
            better_add = randEdge[1]
        elif conf_check[randEdge[1]] == 0 and randEdge[0] not in VertCover:
            better_add = randEdge[0]
        else:
            if dscores[randEdge[0]] > dscores[randEdge[1]]:
                better_add = randEdge[0]
            else:
                better_add = randEdge[1]
        VertCover.append(better_add)
        addV(G, VertCover, conf_check, dscores, edge_weights, uncov_edges, better_add)

        # Update Edge Weights and score functions
        for x in uncov_edges:
            edge_weights[x[1]][x[0]] += 1				
            dscores[x[0]] += 1
        delta_weight += len(uncov_edges)/2

        # If average edge weights of graph above threshold then partially forget prior weighting decisions
        if delta_weight >= E:
            avg_weight +=1
            delta_weight -= E
        if avg_weight > threshold:
            dscores = [0]*(V+1)
            new_tot =0
            uncov_edges = []
            for x in G.edges():
                edge_weights[x[0]][x[1]] = int(reduction_factor*edge_weights[x[0]][x[1]])
                edge_weights[x[1]][x[0]] = int(reduction_factor*edge_weights[x[1]][x[0]])					
                new_tot += edge_weights[x[0]][x[1]]
                if not (x[0] in VertCover or x[1] in VertCover):
                    uncov_edges.append((x[1],x[0]))
                    uncov_edges.append((x[0],x[1]))		
                    dscores[x[0]] += edge_weights[x[0]][x[1]]
                    dscores[x[1]] += edge_weights[x[0]][x[1]]
                elif not (x[0] in VertCover and x[1] in VertCover):
                    if x[0] in VertCover:
                        dscores[x[0]] -= edge_weights[x[0]][x[1]]
                    else:
                        dscores[x[1]] -= edge_weights[x[0]][x[1]]
            avg_weight = new_tot/E
        VertCover = sorted(set(VertCover))		


    #print('LS Solution for ' + str(input_file) + ' ' + str(len(VC_sol)))
    #return VC_sol, trace_output


    total_time = time.time() - start_time

    # Creating the solution and trace files
    vertex_cover=list(VertCover.copy())
    vertex_cover.sort()
    sol += str(len(vertex_cover)) + '\n' + ','.join([str(v) for v in vertex_cover])
    trace += str(total_time) + ', ' + str(len(vertex_cover))
    return sol, trace