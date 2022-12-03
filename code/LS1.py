
# This code is used to perform local search - simulated annealing method

import time
import sys

import math
import random
import argparse
import numpy as np
import networkx as nx

def initial_solution(G, cutoff):
    # create initial solution via removing nodes with more connection (lower bound)
    start_time = time.time()
    _G = list(G.nodes())
    VC = sorted(list(zip(list(dict(G.degree(_G)).values()), _G)), reverse=False)
    i = 0
    while (i < len(VC) and (time.time() - start_time) < cutoff):
        check = True
        for x in G.neighbors(VC[i][1]):
            if x not in _G:
                check = False
        if check:    
            _G.remove(VC[i][1])            
        i += 1
    # fo.write(str(time.time()-start_time) + "," + str(len(_G)) + "\n")
    # print('Initial Solution:({}) {}'.format(len(_G), _G))
    return _G

def LS1_SA(G, cutoff,randSeed):
    T = 0.8 
    random.seed(randSeed)
    S = initial_solution(G, cutoff) 
    start_time = time.time()    
    S_ret = S.copy()
    S_best = []
    sol = ""
    trace = ""
    while ((time.time() - start_time) < cutoff):
        T = 0.95 * T 

        # looking for a better solution with less vertice
        while not S_best:
            S_ret = S.copy()
            trace +=(str(time.time()-start_time) + ", " + str(len(S_ret)) + "\n")
            delete_v = random.choice(S)
            for v in G.neighbors(delete_v):
                if v not in S:
                    S_best.append(v)
                    S_best.append(delete_v)
            S.remove(delete_v)     


        # del node

        S_current = S.copy()
        uncovered_S = S_best.copy()
        delete_v = random.choice(S)
        for v in G.neighbors(delete_v):
            if v not in S:
                S_best.append(v)
                S_best.append(delete_v)            
        S.remove(delete_v)   


        # add node

        add_v = random.choice(S_best)
        S.append(add_v)
        for v in G.neighbors(add_v):
            if v not in S:
                S_best.remove(v)
                S_best.remove(add_v)

        # accept a new solution based on the probability which is proportional to the 
        # difference between the quality of the best solution and the current solution, and the temperature. 
        if len(uncovered_S) < len(S_best): 
            p = math.exp(float(len(uncovered_S) - len(S_best))/T)
            alpha = random.uniform(0, 1)
            if alpha > p:    
                S = S_current.copy()
                S_best = uncovered_S.copy()
    
    sol += str(len(S_best)) + '\n' + ', '.join([str(v) for v in S_best])

    return sol, trace