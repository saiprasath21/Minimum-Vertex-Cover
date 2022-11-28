import time
import random
import math

def LS1_SA(graph, vertices, num_edge, cutoff_time, seed):
    # Simulated annealing
    random.seed(seed)

    start_time = time.time()
    alpha = 0.99  # temp decrease rate
    T0 = 200  # initial temp
    T = T0
    threshold = 1  # define significant improvement
    uncovered = set()  # record uncovered edges
    best_f = len(vertices) # initial score
    trace = [str(round(time.time() - start_time, 2)) + ' ' + str(best_f)] # trace file content

    # all node initialization
    cover = set()
    for i in vertices:
        cover.add(int(i))

    vertices = cover.copy()
    # initialize objective function score
    f = objective(cover, uncovered)
    best_cover = cover.copy()
    best_f = f
    best_f2 = f


    initial_f = best_f2
    while (time.time() - start_time) < cutoff_time: # stop when cut-off time is met
        # Pick a random node to create a neighbor
        u = random.sample(vertices, 1)
        u = int(u[0])

        if u in cover: # if u already in the set, then remove it
            cover.remove(u)
            for i in graph[u]:
                i = int(i)
                if i not in cover:
                    uncovered.add((u, i))
                    uncovered.add((i, u))
        else: # if u not in the set, then add it
            cover.add(u)
            for i in graph[u]:
                i = int(i)
                if i not in cover:
                    uncovered.remove((u, i))
                    uncovered.remove((i, u))


        # Probability computation
        deg_u = len(graph[u])/num_edge
        f1 = objective(cover, uncovered)
        dE = max(0, f1 - f)
        if u in cover:
            P = math.exp(-(dE * (1 - deg_u)) / T)
        else:
            P = math.exp(-(dE * (1 + deg_u)) / T)

        T = T * alpha # update temperature
        rand = random.uniform(0, 1)
        if rand < P:  # admit

            f = f1
        else: # otherwise return back one step
            if u in cover:
                cover.remove(u)
                for i in graph[u]:
                    i = int(i)
                    if i not in cover:
                        uncovered.add((u, i))
                        uncovered.add((i, u))
            else:
                cover.add(u)
                for i in graph[u]:
                    i = int(i)
                    if i not in cover:
                        uncovered.remove((u, i))
                        uncovered.remove((i, u))

        if f < best_f2 and len(uncovered) == 0: # if better and feasible then update results
            best_f2 = f
            best_cover2 = cover.copy()
            if best_f2 < best_f: # if better than best results, then update the best result
                best_f = best_f2
                trace.append(str(round(time.time() - start_time, 2)) + ' ' + str(best_f))
                best_cover = best_cover2.copy()
            if threshold < (initial_f-best_f2): # no significant improvement then restart
                initial_f = best_f2
                T = T0

    return best_cover, trace


def objective(cover, uncovered): # objective function
    a = 1.0
    b = 2.0
    f = a*len(cover)+b*len(uncovered)
    return f