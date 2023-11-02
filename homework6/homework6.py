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
import pandas as pd

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
def maximum_matching(G: nx.Graph):
    flow_graph = G.to_directed()
    left = {x for x,d in flow_graph.nodes(data=True) if d["bipartite"] == 0}
    right = G.nodes() - left
    for x,y,e in flow_graph.edges(data=True):
        if x in left and y in right:
            e["capacity"] = 1
            e["flow"] = 0
        else:
            e["capacity"] = 0
            e["flow"] = 0

    flow_graph.add_node("s")
    flow_graph.add_node("t")

    for x in flow_graph.nodes:
        if "t" != x != "s":
            if x in left:
                flow_graph.add_edge("s",x,capacity=1,flow=0)
            else:
                flow_graph.add_edge(x,"t",capacity=1,flow=0)
    def bfs() -> dict[str,str]:
        queue = deque()
        visited = set()
        prev = {}
        queue.append(("s","s"))
        while queue:
            curr, p = queue.popleft()
            if curr in prev:
                continue
                
            prev[curr] = p
            for x,y,e in flow_graph.edges(curr,data=True):
                if y not in visited and e["capacity"] > e["flow"]:
                    if y == "t":
                        prev["t"] = curr
                        return prev
                    queue.append((y,curr))
                    visited.add(y)
        return prev
    while(True):
        previous_nodes = bfs()
        if "t" not in previous_nodes:
            # no path to destination, we're done
            # could pull min s-t cut by listing keys in prev
            break
        # otherwise, update the flow graph accordingly.
        # because this is matching, the flow is always 1.
        curr = "t"
        prev = previous_nodes[curr]
        while prev != curr:
            flow_graph[prev][curr]["flow"] += 1
            # no backward flow updates on (*, s) or (t, *)
            if curr != 't' and prev != 's':
                flow_graph[curr][prev]["flow"] -= 1
            curr = prev
            prev = previous_nodes[curr]
    
    # we can read off the matching by determining what edges from set left to set right have flow = 1
    matching = {}
    matching_edgelist = []
    for x,y,e in flow_graph.edges(data=True):
        if x in left and e["flow"] != 0:
            matching[x] = y    
            matching[y] = x
            matching_edgelist.append((x,y))

    pos = nx.bipartite_layout(G, left)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, width=0.3)
    nx.draw_networkx(G, pos, edgelist=matching_edgelist, edge_color="red", width=3)
    plt.axis("off")
    plt.savefig('bipartite.png')
    
    return matching

            





'''
Problems 2 and 3
Implement Karger's min-cut algorithm
Note: the input is a multi-graph
On each input graph, run 200 iterations of Kargers, report the minimum cut size, and plot a distribution of cut sizes across iterations
I suggest using plotnine for this, a python implementation of ggplot 
'''
def Kargers(G: nx.MultiGraph, filename: str):
    def contract(H: nx.MultiGraph, x, y):
        for _,b in list(H.edges(y)):
            if b == x:
                continue
            H.add_edge(x,b)
        H.remove_node(y)
    ITERS = 200
    min_cuts = []
    for _ in range(ITERS):
        H = G.copy()
        num_nodes = len(H.nodes)
        while num_nodes > 2:
            x,y,z = random.choice([*H.edges])
            #H = nx.contracted_edge(H, (x,y,z), self_loops = False)
            contract(H, x, y)
            num_nodes = len(H.nodes)
        print(len(H.edges), end=" ")
        min_cuts.append(len(H.edges))
    p = (
        ggplot(aes(x="Min Cut Size"), pd.DataFrame({"Min Cut Size": min_cuts}))
        + geom_histogram(binwidth=1)
    )
    p.save(filename)
    print("Best Min Cut:", min(min_cuts))
        









# make graph and run functions
bipartite_graph = bipartite.random_graph(12,12,0.2,seed=4) # random seed guaranteed to be random, chosen by fair dice roll https://xkcd.com/221/

m = maximum_matching(bipartite_graph)
left = {x for x,d in bipartite_graph.nodes(data=True) if d["bipartite"] == 0}
print("Max Cardinality Matching:", {x:m[x] for x in sorted(m) if x in left})
# m2 = bipartite.hopcroft_karp_matching(bipartite_graph, left)
# print(m,m2,m==m2, sep='\n')

# I make a complete graph and remove a lot of edges

G = nx.complete_graph(100)

random.seed(4)



for (x,y) in G.edges:
    if random.random() > 0.1:
        G.remove_edge(x,y)

G = nx.MultiGraph(G)

# I make a complete graph and remove more edges between two sets of nodes than within those sets
G2 = nx.complete_graph(100)

for (x,y) in G2.edges:
    # print(x,y)
    if (x < 50 and y > 50) or (x > 50 and y < 50):
        if random.random() > 0.05:
            # print("yes")
            G2.remove_edge(x,y)
    else:
        if random.random() > 0.4:
            # print("and_yes")
            G2.remove_edge(x,y)

G2 = nx.MultiGraph(G2)
Kargers(G, "kargers_G.png")
Kargers(G2, "kargers_G2.png")
