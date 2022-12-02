from time import time
import networkx as nx
import numpy as np

def removeFalse(optimalVC : list):
    for ele in optimalVC:
        if not ele[1]:
            optimalVC.remove(ele)
    return optimalVC

def BNB(bnbGraph, timeLimit):
    timeLimit = int(timeLimit)
    startTime = time()
    timeTaken = 0 
    times = []
    allVC = []
    currGraph:nx.Graph=bnbGraph.copy() #maintain a copy that can be modified / replaced...
    #find node with maximum degree... use separate function..?
    #####...max degree...####
    # print(dict(currGraph.degree()))
    list_of_degrees=sorted(dict(currGraph.degree()).items(), reverse=True, key=lambda item: item[1])
    max_node, maxDegree=list_of_degrees[0] #this is a tuple...(node, degree)
    optimalVC=np.array([])
    currVC=[]
    frontier=[]
    # neighbours=[]
    upperBound=currGraph.number_of_nodes()
    print('Initial UpperBound:', upperBound)
    #lower bound calc later..
    frontier.append([max_node, False, -1, None]) #1st parent's val: -1, -1..? #0: False... 1: True...
    frontier.append([max_node, True, -1, None])
    #2 different possibilities added to frontier...
    while len(frontier)!=0 and timeTaken < timeLimit:
        poppedVertex, considered, parent_node, parent_node_considered=frontier.pop()
        #backtrack flag..? instead just call backtracking func..?
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
                optimalVC=np.array(removeFalse(currVC.copy()))
                upperBound=count
                print('Current Opt VC size', count)
                times.append((count, time()-startTime))
                allVC.append(list(optimalVC[:,0]))
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
                
    return list(optimalVC[:,0]), (allVC,times)

