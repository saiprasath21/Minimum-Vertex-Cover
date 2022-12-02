import time
import random
import networkx as nx
import numpy as np
from Approx import Approx


def init(G, start_time, cutoff, trace_output):
    temp_G = G.nodes()
    VC = sorted(list(zip(list(dict(G.degree(temp_G)).values()), temp_G)))
    VC_sol = temp_G
    i=0
    uncovE=[]
    optvc_len = len(VC_sol)
    while(i < len(VC) and (time.time() - start_time) < cutoff):
        flag=True
        for x in G.neighbors(VC[i][1]):
            if x not in temp_G:
                flag = False
        if flag:	
            list(temp_G).remove(VC[i][1])
        i=i+1
    return VC_sol, trace_output	

# Helper method to add a vertex
def addV(G, VC, conf_check, dscores, edge_weights, uncovE, add):
    dscores[add] = -dscores[add]
    for x in G.neighbors(add):
        if x not in VC:
            uncovE.remove((add,x))
            uncovE.remove((x,add))
            conf_check[x] = 1
            dscores[x] -= edge_weights[add][x]
        else:
            dscores[x] += edge_weights[add][x]

# Helper method to remove a vertex
def removeV(G, VC, conf_check, dscores, edge_weights, uncovE, removed):
    dscores[removed] = -dscores[removed]
    conf_check[removed] = 0
    for x in G.neighbors(removed):
        if x not in VC:
            uncovE.append((removed,x))
            uncovE.append((x,removed))
            conf_check[x] = 1
            dscores[x] += edge_weights[removed][x]
        else:
            dscores[x] -= edge_weights[removed][x]

# Helper method to verify a vertex cover
def check(Gx, VC):
    #print("Initial: ", np.shape(Gx.edges()))
    for v in VC:
        Gx.remove_node(v)
    if len(Gx.edges())>0:
        print("Checked: Graph is not a Vertex Cover")
    else:
        print("Checked: Graph is a Vertex Cover (VC)")
    #print("Final: ", np.shape(Gx.edges()))

#Hill CLimb Implementation
def Hill(G, V, E, randSeed,cutoff):
    # Initialization

    #Computing Initial Solution
    vertex_coverx, trace_output, vertex_cover = Approx(G,True)#init(G, start_time, cutoff, trace_output)
    

    #Declaration of variables
    trace_output=""#[]

    start_time = time.time()
    sol = ""
    trace = ""

    random.seed(randSeed)

    threshold = .5*V
    reduction_factor = .3

    edge_weights = nx.convert.to_dict_of_dicts(G, edge_data=1)

    conf_check = [1]*(V+1)
    dscores = [0]*(V+1)
    uncovE=[]

    VC=list(vertex_cover)
    VC_sol = VC.copy()
    optvc_len = len(VC)
    avg_weight = 0
    delta_weight = 0
    Gi=G.copy()

    #andHereWeGoAgain

    while((time.time() - start_time) < cutoff):	

        # If it is a vertex cover: remove the max cost node		
        while not uncovE:
            if (optvc_len > len(VC)):
                total_time = time.time() - start_time
                trace_output += str(total_time) + ', ' + str(optvc_len)
                #trace_output.append((optvc_len,time.time()-start_time))					
                VC_sol = VC.copy()	
                optvc_len = len(VC)
            max_improv = -float('inf')
            for x in VC:
                if dscores[x] > max_improv:
                    max_improv = dscores[x]
                    opt_rem = x
            VC.remove(opt_rem)
            removeV(G, VC, conf_check, dscores, edge_weights, uncovE, opt_rem)


        # remove max cost node from solution
        max_improv = -float('inf')
        for x in VC:
            if dscores[x] > max_improv:
                max_improv = dscores[x]
                opt_rem = x
        VC.remove(opt_rem)
        removeV(G, VC, conf_check, dscores, edge_weights, uncovE, opt_rem)



        # find node from random uncovered edge to add
        randEdge = random.choice(uncovE)
        if conf_check[randEdge[0]] == 0 and randEdge[1] not in VC: 
            better_add = randEdge[1]
        elif conf_check[randEdge[1]] == 0 and randEdge[0] not in VC:
            better_add = randEdge[0]
        else:
            if dscores[randEdge[0]] > dscores[randEdge[1]]:
                better_add = randEdge[0]
            else:
                better_add = randEdge[1]
        VC.append(better_add)
        addV(G, VC, conf_check, dscores, edge_weights, uncovE, better_add)

        # Update Edge Weights and score functions
        for x in uncovE:
            edge_weights[x[1]][x[0]] += 1				
            dscores[x[0]] += 1
        delta_weight += len(uncovE)/2

        # If average edge weights of graph above threshold then partially forget prior weighting decisions
        if delta_weight >= E:
            avg_weight +=1
            delta_weight -= E
        if avg_weight > threshold:
            dscores = [0]*(V+1)
            new_tot =0
            uncovE = []
            for x in G.edges():
                edge_weights[x[0]][x[1]] = int(reduction_factor*edge_weights[x[0]][x[1]])
                edge_weights[x[1]][x[0]] = int(reduction_factor*edge_weights[x[1]][x[0]])					
                new_tot += edge_weights[x[0]][x[1]]
                if not (x[0] in VC or x[1] in VC):
                    uncovE.append((x[1],x[0]))
                    uncovE.append((x[0],x[1]))		
                    dscores[x[0]] += edge_weights[x[0]][x[1]]
                    dscores[x[1]] += edge_weights[x[0]][x[1]]
                elif not (x[0] in VC and x[1] in VC):
                    if x[0] in VC:
                        dscores[x[0]] -= edge_weights[x[0]][x[1]]
                    else:
                        dscores[x[1]] -= edge_weights[x[0]][x[1]]
            avg_weight = new_tot/E
        VC = sorted(set(VC))		

        #total_time = time.time() - start_time
        #trace_output += str(total_time) + ', ' + str(len(vertex_cover))

    # Creating the solution and trace files
    vertex_cover=list(VC_sol.copy())
    vertex_cover.sort()
    sol += str(len(vertex_cover)) + '\n' + ','.join([str(v) for v in vertex_cover])

    G_=G

    check(G_,VC_sol.copy())

    return sol, trace_output