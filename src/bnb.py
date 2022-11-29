import argparse
import os
from time import time
import networkx as nx


#python bnb2.py -inst DATA/email.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/dummy1.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/dummy2.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/jazz.graph -alg BnB -time 600 -seed 100 

#python bnb2.py -inst DATA/power.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/star.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/star2.graph -alg BnB -time 600 -seed 100 

#python bnb2.py -inst DATA/netscience.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/karate.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/hep-th.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/football.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/delaunay_n10.graph -alg BnB -time 600 -seed 100 
#python bnb2.py -inst DATA/as-22july06.graph -alg BnB -time 600 -seed 100 
def parse_file(filename):
    adjacency_list=[]
    new_graph=nx.Graph()
    with open(filename) as file1:
        first_row=file1.readline().split()
        # print(first_row)
        vertex_count=int(first_row[0])
        for i in range(vertex_count):
            each_line=file1.readline().split()
            # each_line=[int(x) for x in each_line]
            each_line=list(map(int, each_line))
            for elem in each_line:
                new_graph.add_edge(i+1, elem)
            # print(list(each_line))
            adjacency_list.append(each_line)
    return new_graph #, adjacency_list

# def get_node_max_degree(curr_graph):
#     list_of_degrees=curr_graph.degree()

def bnb(filename, timeLimit):
    startTime = time()
    timeTaken = 0 
    times = []
    bnbGraph=parse_file(filename)
    brrr = bnbGraph.copy()
    currGraph:nx.Graph=bnbGraph.copy() #maintain a copy that can be modified / replaced...
    #find node with maximum degree... use separate function..?
    #####...max degree...####
    # print(dict(currGraph.degree()))
    list_of_degrees=sorted(dict(currGraph.degree()).items(), reverse=True, key=lambda item: item[1])
    max_node, maxDegree=list_of_degrees[0] #this is a tuple...(node, degree)
    optimalVC=[]
    currVC=[]
    frontier=[]
    upperBound=currGraph.number_of_nodes()
    print('upperbound (initial):', upperBound)
    #lower bound calc later..
    frontier.append([max_node, False, -1, None]) #1st parent's val: -1, -1..? #0: False... 1: True...
    frontier.append([max_node, True, -1, None])
    #2 different possibilities added to frontier...
    while len(frontier)!=0 and timeTaken < timeLimit:
        poppedVertex, considered, parent_node, parent_node_considered=frontier.pop()
        
        if considered:
            currGraph.remove_node(poppedVertex)
        else:
            # popped_vertex_neighbours=curr_graph.neighbors(max_node)
            for elem in list(currGraph.neighbors(poppedVertex)): #change made: list of neighs...
                currVC.append([elem, True])
                currGraph.remove_node(elem)
        currVC.append([poppedVertex, considered])
        count=0
        for elem in currVC:
            if elem[1]:
                count+=1

        if currGraph.number_of_edges()==0:
            if count<upperBound:
                optimalVC=currVC.copy()
                upperBound=count
                print('size of current VC (optimal)', count)
                times.append((count, time()-startTime))
            #backtracking...
            if len(frontier)!=0:
                if [frontier[-1][2], frontier[-1][3]] in currVC: #change made: tuple to list..
                    index=-1
                    for i in range (len(currVC)):
                        if currVC[i]==[frontier[-1][2], frontier[-1][3]]: #change made: tuple to list [-1][2]...
                            index=i+1
                            break
                    if index>-1:
                        while index<len(currVC):
                            currNode, currConsidered=currVC.pop()
                            currGraph.add_node(currNode)
                            currVCNodes=[]
                            for i in range (len(currVC)):
                                currVCNodes.append(currVC[i][0])
                            for neigh in bnbGraph.neighbors(currNode):
                                if (neigh in currGraph.nodes()) and (neigh not in currVCNodes):
                                    currGraph.add_edge(neigh, currNode)
                                

                elif frontier[-1][2]==-1 and frontier[-1][3] is None:
                    currVC.clear()
                    currGraph=bnbGraph.copy()

                else:
                    print("Error...")
            
        else:
            #find lower bound then add count to it...
            bound=currGraph.number_of_edges()/maxDegree
            bound+=count
            if bound<upperBound:
                poppedVertex2= sorted(dict(currGraph.degree()).items(), reverse=True, key=lambda item: item[1])[0] #max degree node again..
                frontier.append([poppedVertex2[0], False, poppedVertex, considered])
                frontier.append([poppedVertex2[0], True, poppedVertex, considered])
            else:
                if len(frontier)!=0: #change made: included if statement..
                #backtracking code...
                    if [frontier[-1][2], frontier[-1][3]] in currVC: #change made: tuple to list..
                        index=-1
                        for i in range (len(currVC)):
                            if currVC[i]==[frontier[-1][2], frontier[-1][3]]: #change made: tuple to list of parent params...
                                index=i+1
                                break
                        if index>-1:
                            while index<len(currVC):
                                currNode, currConsidered=currVC.pop()
                                currGraph.add_node(currNode)
                                currVCNodes=[]
                                for i in range (len(currVC)):
                                    currVCNodes.append(currVC[i][0])
                                for neigh in bnbGraph.neighbors(currNode):
                                    if (neigh in currGraph.nodes()) and (neigh not in currVCNodes):
                                        currGraph.add_edge(neigh, currNode)
                                    

                    elif frontier[-1][2]==-1 and frontier[-1][3]is None:
                        currVC.clear()
                        currGraph=bnbGraph.copy()

                    else:
                        print("Error2...")
        timeTaken = time()-startTime
        if timeTaken > timeLimit:
            print("Time limit reached")
                
    return optimalVC, times

def main(inputFilename, output_dir, cutoff, randseed, algorithm):
    optimalVC, times = bnb(inputFilename, cutoff)
    print(optimalVC)
    for ele in optimalVC:
        if not ele[1]:
            optimalVC.remove(ele)
    print(optimalVC)

    # outfileHeader = inputFilename.split(".")[0]
    outfileHeader = inputFilename.split(".")[0].split("/")[-1]

    #sol files
    with open(f"./{output_dir}/{outfileHeader}_{algorithm}_{cutoff}.sol", 'w') as f:
        f.write(str(len(optimalVC))+"\n")
        f.write(",".join([str(x[0]) for x in optimalVC]))
    
    #trace files
    with open(f"./{output_dir}/{outfileHeader}_{algorithm}_{cutoff}.trace", 'w') as f:
        for i in times:
            f.write('%.2f,%i\n' % ((i[1]),i[0]))

# _, adj_list=parse_file("dummy1.graph")
# print(adj_list)
if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Input parser for BnB')
    parser.add_argument('-inst',action='store',type=str,required=True,help='Inputgraph datafile')
    parser.add_argument('-algo',action='store',default=1000,type=str,required=True,help='Name of algorithm')
    parser.add_argument('-time',action='store',default=1000,type=int,required=True,help='Cutoff running time for algorithm')
    parser.add_argument('-seed',action='store',default=1000,type=int,required=False,help='random seed')
    args=parser.parse_args()

    algorithm = args.algo
    graph_file = args.inst
    output_dir = 'Output/'
    cutoff = args.time
    randSeed = args.seed

    main(graph_file,output_dir,cutoff,randSeed,algorithm)
