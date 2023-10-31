'''
COMP 5970/6970 Graph Algorithms Homework 4 coding section
requires networkx, argparse
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
'''

import argparse
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import numpy as np
from plotnine import *
from networkx.algorithms import bipartite
import random
from collections import deque

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement maximum cardinality matching given a bipartite graph.
Feel free to use either Hopcraft-Karp or Edmonds-Karp
The nodes will have an attribute "bipartite" with values 0 or 1 
Output a picture of the graph with edges in the matching in a different color
Use the bipartite_layout to draw it.
'''
def maximum_matching(G):
    flow_graph = G.copy()
    to_add = []
    # print(flow_graph.edges(data=True))
    for x,y,e in flow_graph.edges(data=True):
        e["capacity"] = 1
        e["flow"] = 0
        e["revere_capacity"] = 0
        e["reverse_flow"] = 0
        # to_add.append((y,x))
    # flow_graph.add_edges_from(to_add, flow=0, capacity=0)

    print(flow_graph.edges(data=True))
    flow_graph.add_node("s")
    flow_graph.add_node("t")

    for x, d in flow_graph.nodes(data=True):
        if d["bipartite"] == 0:
            flow_graph.add_edge("s",x,capacity=1,flow=0)
        else:
            flow_graph.add_edge(x,"t",capacity=1,flow=0)

    print(flow_graph.edges(data=True))
    def bfs():
        queue = deque()
        visited = set()
        prev = {}
        queue.append(("s","s"))
        while queue:
            curr, p = queue.popleft()
            


    print("make a matching")



'''
Problems 2 and 3
Implement Karger's min-cut algorithm
Note: the input is a multi-graph
On each input graph, run 200 iterations of Kargers, report the minimum cut size, and plot a distribution of cut sizes across iterations
I suggest using plotnine for this, a python implementation of ggplot 
'''
def Kargers(G):
    print("find minimum cuts")







# make graph and run functions
bipartite_graph = bipartite.random_graph(12,12,0.2,seed=4) # random seed guaranteed to be random, chosen by fair dice roll https://xkcd.com/221/

maximum_matching(bipartite_graph)

# # I make a complete graph and remove a lot of edges

# G = nx.complete_graph(100)

# random.seed(4)



# for (x,y) in G.edges:
#     if random.random() > 0.1:
#         G.remove_edge(x,y)

# G = nx.MultiGraph(G)

# # I make a complete graph and remove more edges between two sets of nodes than within those sets
# G2 = nx.complete_graph(100)

# for (x,y) in G2.edges:
#     print(x,y)
#     if (x < 50 and y > 50) or (x > 50 and y < 50):
#         if random.random() > 0.05:
#             print("yes")
#             G2.remove_edge(x,y)
#     else:
#         if random.random() > 0.4:
#             print("and_yes")
#             G2.remove_edge(x,y)

# G2 = nx.MultiGraph(G2)

# Kargers(G)
# Kargers(G2)
