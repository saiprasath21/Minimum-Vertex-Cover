# This code implements the Branch and Bound approach for finding the MVC. 
from time import time
import networkx as nx
import numpy as np

#function to remove elements from optimal vc if they are not in the "considered" state
def removeFalse(optimalVC : list):
    for ele in optimalVC:
        if not ele[1]:
            optimalVC.remove(ele)
    return optimalVC

#branch and bound function
def BNB(bnbGraph, timeLimit):
    timeLimit = int(timeLimit)
    startTime = time()
    timeTaken = 0 
    times = []
    currGraph:nx.Graph=bnbGraph.copy() #maintain a copy that can be modified / replaced...
    #find node with maximum degree
    # print(dict(currGraph.degree()))
    list_of_degrees=sorted(dict(currGraph.degree()).items(), reverse=True, key=lambda item: item[1])
    max_node, maxDegree=list_of_degrees[0] #this is a tuple...(node, degree)
    optimalVC=np.array([])
    currVC=[]
    frontier=[]
    upperBound=currGraph.number_of_nodes()
    print('Initial UpperBound:', upperBound)
    frontier.append([max_node, False, -1, None]) #1st parent's val: -1, None
    frontier.append([max_node, True, -1, None])
    #2 different possibilities added to frontier ^^...
    while len(frontier)!=0 and timeTaken < timeLimit:
        poppedVertex, considered, parent_node, parent_node_considered=frontier.pop()
        if considered:
            currGraph.remove_node(poppedVertex)
        else:
            # add neighbours of popped vertex to currVC then remove those vertices from graph
            for elem in list(currGraph.neighbors(poppedVertex)): #change made: list of neighs...
                currVC.append([elem, True])
                currGraph.remove_node(elem)
        currVC.append([poppedVertex, considered])
        count=0 #count=considered vertices in currvc
        for elem in currVC:
            if elem[1]:
                count+=1

        if currGraph.number_of_edges()==0:
            if count<upperBound:
                optimalVC=np.array(removeFalse(currVC.copy()))
                upperBound=count
                print('Current Opt VC size', count)
                times.append((time()-startTime, count))
            #backtracking code...
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
                    print("Error")
            
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
                        print("Error")
                        
        timeTaken = time()-startTime
        if timeTaken > timeLimit:
            print("Time limit reached")
    sol = ""
    sol += str(len(list(optimalVC[:,0]))) + '\n' + ','.join([str(v) for v in sorted(list(optimalVC[:,0]))])
    trace = ""
    for i in range(len(times)):
        trace += f"{times[i][0]}, {times[i][1]}\n"

    return sol, trace
