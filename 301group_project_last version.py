#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import time
import timeit
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')

plt.rcParams["figure.figsize"] = [7,7]
# plt.rcParams["figure.figsize"] = [4,4]


# In[ ]:


runtime_dataframe = pd.DataFrame()


# In[ ]:


running_time_vector_5 = []
running_time_vector_6 = []
running_time_vector_7 = []
running_time_vector_8 = []
running_time_vector_9 = []
running_time_vector_10 = []
running_time_vector_15 = []
running_time_vector_20 = []
running_time_vector_25 = []
mylist = {'5' : 0 , '6' : 0 , '7' : 0 , '8' : 0, '9' : 0 , '10' : 0 , '15' : 0 , '20' : 0 }


# In[ ]:


success_dataframe = pd.DataFrame()
success_vector5 = []
success_vector6 = []
success_vector7 = []
success_vector8 = []
success_vector9 = []
success_vector10 = []
success_vector15 = []
success_vector20 = []


# In[ ]:


import random
import math
import time

def decreaseTemperature(initialTemperature, i):
    return initialTemperature / i

def getTransitionProbability(dE, T):
    return math.exp(-dE / T)

def isTransition(probability):
    trigger = random.uniform(0, 1)
    
    if trigger < probability:
        return True
    else:
        return False

def calculateEnergy(path):
    pathPairs = list(zip(path[0::1],path[1::1]))
    energy = len(pathPairs)
    return energy

def generateStateCandidate(path, availableEdges, G):
    if len(path) == 1: # Path is equal to node
        path = list(random.choice(availableEdges)) # Take any edge as a new path
        availableEdges = []
        for edge in G.edges():
            availableEdges.append(edge)
            availableEdges.append(edge[::-1])
        availableEdges.remove(tuple(path))
        availableEdges.remove(tuple(path[::-1]))

    if random.choice([True, True, False]): # Add new edge
    
        if not availableEdges: # All edges are in path
#             print "No available edges"
            return path, availableEdges
            
        # Path consists from one edge or more
        if random.choice([True, False]): # Add edge to the start
#             print "Add to start"
            nodeCandidates = list(G.nodes())
            random.shuffle(nodeCandidates)
            for node in nodeCandidates:
                if (node, path[0]) in availableEdges and (path[0], node) in availableEdges and node != path[-1] and node not in path:
#                     print "Adding node - ", node
                    path.insert(0, node)
#                     print "New path - ", path
                    availableEdges.remove((path[0], path[1]))
                    availableEdges.remove((path[1], path[0]))
                    break
        else: # Add edge to the end
#             print "Add to end"
            nodeCandidates = list(G.nodes())
            random.shuffle(nodeCandidates)
            for node in nodeCandidates:
                if (node, path[-1]) in availableEdges and (path[-1], node) in availableEdges and node != path[0] and node not in path:
#                     print "Adding node - ", node
                    path.append(node)
#                     print "New path - ", path
                    availableEdges.remove((path[-1], path[-2]))
                    availableEdges.remove((path[-2], path[-1]))
                    break
        
    else: # Remove edge
        if random.choice([True, False]): # Remove start edge
#             print "Remove start node - ", path[0]
            availableEdges.append((path[0], path[1]))
            availableEdges.append((path[1], path[0]))
            path.pop(0)
        else: # Remove end edge
#             print "Remove end node - ", path[-1]
            availableEdges.append((path[-1], path[-2]))
            availableEdges.append((path[-2], path[-1]))
            path.pop(-1)
    
    return path, availableEdges


# ## Generate random graph and the longest simple  path containing at least k edges¶ 

# In[ ]:


for i in range(100) :  
       start = timeit.default_timer()
       try :
           # Random graph
           G = nx.fast_gnp_random_graph(20, 0.65)
           pos = nx.spring_layout(G)

           # Random path
           startPoint, finishPoint = random.choice(list(G.nodes())), random.choice(list(G.nodes()))
           print("startpoint: ",startPoint)
           print("finishpoint: ",finishPoint)

           paths = list(nx.all_simple_paths(G, startPoint, finishPoint))
           if paths:
               # currentPathRandom = random.choice(paths)
               currentPathRandom = list(random.choice(list(G.edges()))) # Use random edge cause simple path usually too long
           else:
               currentPathRandom = list(list(G.edges()[0]))

           currentPathPairs = zip(currentPathRandom[0::1],currentPathRandom[1::1])

           labels = {x : str(x) for x in G.nodes()}

           nx.draw_networkx_nodes(G, pos = pos, node_color = "green", node_size = 600, with_labels=False)
           nx.draw_networkx_nodes(G, pos = pos, node_color = "blue", node_size = 600, nodelist = currentPathRandom, with_labels=False)
           nx.draw_networkx_labels(G,pos, labels, font_color = "white", font_size = 15)

           nx.draw_networkx_edges(G, pos = pos, width = 3, edge_color = "green")
           nx.draw_networkx_edges(G, pos = pos, width = 3, edge_color = "blue", edgelist = list(currentPathPairs))

           timestamp = str(time.time())

           plt.axis('off')
           #plt.savefig("graph_pictures/{}_RANDOM_PATH.png".format(timestamp), format = "PNG")
           plt.show()

           # List of edges not used in current path
           nonUsedEdges = []
           for edge in G.edges():
               if edge not in currentPathPairs and edge[::-1] not in currentPathPairs:
                   nonUsedEdges.append(edge)
                   nonUsedEdges.append(edge[::-1])

           print (G.edges())



           currentPath = currentPathRandom

           currentEnergy = calculateEnergy(currentPath)
           initialTemperature = 100000
           endTemperature = 1
           T = initialTemperature

           for i in range(1, 10000):
               stateCandidate, newNonUsedEdges = generateStateCandidate(currentPath, nonUsedEdges, G)
               candidateEnergy = calculateEnergy(stateCandidate)

               if candidateEnergy >= currentEnergy:
                   currentPath = stateCandidate
                   currentEnergy = candidateEnergy
                   nonUsedEdges = newNonUsedEdges
               else:
                   p = getTransitionProbability(currentEnergy - candidateEnergy, T)
                   if isTransition(p):
                       currentPath = stateCandidate
                       currentEnergy = candidateEnergy
                       nonUsedEdges = newNonUsedEdges
               T = decreaseTemperature(initialTemperature, i)
               if T <= endTemperature:
                   break
           
           for i in range(1,len(currentPath)) : # choose k
               
               k  = i # choose k equal to i for trying all possible values
                      # for obtaining a success rate 
                      # at last, we are trying to obtain a longest simple path containing k edges.
               nx.draw_networkx_nodes(G, pos = pos, node_color = "green", node_size = 600, with_labels=False)
               nx.draw_networkx_nodes(G, pos = pos, node_color = "blue", node_size = 600, nodelist = currentPath, with_labels=False)
               nx.draw_networkx_labels(G,pos, labels, font_color = "white", font_size = 15)

               currentPathPairs = zip(currentPath[0::1],currentPath[1::1])
               nx.draw_networkx_edges(G, pos = pos, width = 3, edge_color = "green")
               nx.draw_networkx_edges(G, pos = pos, width = 3, edge_color = "blue", edgelist = list(currentPathPairs))

               plt.axis('off')
               #plt.savefig("graph_pictures/{}_METROPOLIS_WITH_ANNEALING.png".format(timestamp), format = "PNG")
               plt.show()



           currentPath = currentPathRandom

           currentEnergy = calculateEnergy(currentPath)
           initialTemperature = 100
           endTemperature = 1
           T = initialTemperature

           for i in range(1, 10000):
               stateCandidate, newNonUsedEdges = generateStateCandidate(currentPath, nonUsedEdges, G)
               candidateEnergy = calculateEnergy(stateCandidate)

               if candidateEnergy >= currentEnergy:
                   currentPath = stateCandidate
                   currentEnergy = candidateEnergy
                   nonUsedEdges = newNonUsedEdges
               else:
                   p = getTransitionProbability(currentEnergy - candidateEnergy, T)
                   if isTransition(p):
                       currentPath = stateCandidate
                       currentEnergy = candidateEnergy
                       nonUsedEdges = newNonUsedEdges
           #     T = decreaseTemperature(initialTemperature, i)
               if T <= endTemperature:
                   break

           nx.draw_networkx_nodes(G, pos = pos, node_color = "green", node_size = 600, with_labels=False)
           nx.draw_networkx_nodes(G, pos = pos, node_color = "blue", node_size = 600, nodelist = currentPath, with_labels=False)
           nx.draw_networkx_labels(G,pos, labels, font_color = "white", font_size = 15)

           currentPathPairs = zip(currentPath[0::1],currentPath[1::1])
           nx.draw_networkx_edges(G, pos = pos, width = 3, edge_color = "green")
           nx.draw_networkx_edges(G, pos = pos, width = 3, edge_color = "blue", edgelist = list(currentPathPairs))
           
           success_vector20.append(True)
           plt.axis('off')
           #plt.savefig("graph_pictures/{}_METROPOLIS_WITHOUT_ANNEALING.png".format(timestamp), format = "PNG")
           plt.show()
       except :
           success_vector20.append(False)
           print("can not generate a longest simple path, exiting...")
       end = timeit.default_timer()
       running_time_vector_20.append(end-start)
       


# In[ ]:


runtime_dataframe['5 vertice Runtimes'] = running_time_vector_5
runtime_dataframe['6 vertice Runtimes'] = running_time_vector_6
runtime_dataframe['7 vertice Runtimes'] = running_time_vector_7
runtime_dataframe['8 vertice Runtimes'] = running_time_vector_8
runtime_dataframe['9 vertice Runtimes'] = running_time_vector_9
runtime_dataframe['10 vertice Runtimes'] = running_time_vector_10
runtime_dataframe['15 vertice Runtimes'] = running_time_vector_15
runtime_dataframe['20 vertice Runtimes'] = running_time_vector_20


# In[ ]:


success_dataframe['5 vertice'] = success_vector5
success_dataframe['6 vertice'] = success_vector6
success_dataframe['7 vertice'] = success_vector7
success_dataframe['8 vertice'] = success_vector8
success_dataframe['9 vertice'] = success_vector9
success_dataframe['10 vertice'] = success_vector10
success_dataframe['15 vertice'] = success_vector15
success_dataframe['20 vertice'] = success_vector20


# In[ ]:





# In[ ]:


runtime_dataframe.to_excel("500_graph_generated.xlsx")


# In[ ]:


success_dataframe.to_excel("500_success.xlsx")

