'''
COMP 5970/6970 Graph Algorithms Homework 2 coding section
requires networkx, argparse
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
'''

import argparse
import networkx as nx
import pickle
import matplotlib.pyplot as plt
from collections import defaultdict
import math

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement topological sort on the nodes of the graph G
'''
def TarjansCycleDetect(G):
    visited = set()
    on_stack = set()
    low_link = {}
    index = {}
    node_index_so_far = 0
    def dfs(G, v, node_index):
        index[v] = node_index
        node_index += 1
        low_link[v] = index[v]
        on_stack.add(v)
        visited.add(v)
        for x in G.adj[v]:
            if x not in visited:
                return dfs(G, x, node_index)
            if x in on_stack:
                low_link[x] = min(low_link[v], low_link[x])
        if low_link[v] == index[v]:
            return False
        return True

    
    for v in G.nodes:
        if v not in visited:
            if dfs(G,v, node_index_so_far):
                return True
    return False

def topological_sort(G):
    # first, determine if the nodes have cycle
    if TarjansCycleDetect(G):
        print("CYCLE FOUND")
        return
    stack = []
    visited = set()

    def dfs(v):
        for x in G.neighbors(v):
            if x not in visited:
                dfs(x)
        stack.append(v)
        visited.add(v)
    for v in G.nodes:
        if v not in visited:
            dfs(v)
    # print([*reversed(stack)])
    return [*reversed(stack)]
    

    





'''
Problem 2
Find the longest path in the directed acyclic graph
output the labels of the traversed edges and the alignment they imply
(edges are labeled with tuples, build up 2 strings from these and output on separate lines)
(example if i had path with edge labels (-,G),(A,A) then I want the following output
-A
GA
'''
def longest_path(G):
    V = topological_sort(G)
    value = defaultdict(lambda: 1e-9)
    parent = {}
    for v in V:
        value[v] = 0
        parent[v] = None
        for x,_,data in G.in_edges(v, data=True):
            weight = data['weight']
            if value[x] + weight > value[v]:
                value[v] = value[x] + weight
                parent[v] = x
    v = max(G.nodes, key=lambda x: value[x])
    # print(value)

    path = []
    while v is not None:
        path.append(v)
        v = parent[v]
    path = path[::-1]
    res = []
    for i in range(len(path)-1):
        start, end = path[i], path[i+1]
        res.append(G[start][end]['label'])
    reshaped_res = [*zip(*res)]
    print("Longest path alignment is")
    for i in range(len(reshaped_res[0])):
        print(str(reshaped_res[0][i]) + str(reshaped_res[1][i]))






# make graph and run functions

s1 = "GTCGTAGAATA"
s2 = "GTAGTAGATA"
G = nx.DiGraph()
for i in range(len(s1)+1):
    for j in range(len(s2)+1):
        G.add_node((i,j))
print(G.nodes)
print(len(G.nodes))

for i in range(1,len(s1)+1):
    G.add_edge((i-1,0),(i,0), weight=-1, label=(s1[i-1],"-"))
for j in range(1,len(s2)+1):
    G.add_edge((0,j-1),(0,j), weight=-1, label=("-",s2[j-1]))

for i in range(1,len(s1)+1):
    for j in range(1,len(s2)+1):
        # add 3 edges, one from left, one from up, and one from diagonal up left
        G.add_edge((i-1,j),(i,j),weight=-1,label=(s1[i-1],"-"))
        G.add_edge((i,j-1),(i,j),weight=-1,label=("-",s2[j-1]))
        score = -1
        if s1[i-1] == s2[j-1]:
            score = 1
        G.add_edge((i-1,j-1),(i,j),weight=score, label=(s1[i-1],s2[j-1]))


print(len(G.edges))
longest_path(G)
