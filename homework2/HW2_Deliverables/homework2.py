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

parser = argparse.ArgumentParser()
parser.add_argument("--graph", help="file containing graph in pickle format for problem 1")
args = parser.parse_args()

'''
Problem 1
Implement the disjoint-set / union-find data structure with path compression
'''
class DisjointSet:
    # data structure to back the disjoint set here (you can use an array, a dict, or you could use a graph)
    
    def __init__(self):
        self.parents = {}

    def makeset(self, x):
        self.parents[x] = x
    
    def find(self, x):
        if self.parents[x] == x:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        px, py = map(self.find, (x,y))
        self.parents[py] = px if px != py else None

'''
Problem 2
find the minimum spanning tree of G using your disjoint set data structure above
then draw the graph with the edges in the MST twice as thick as the other edges and save that to mst.png

some code I used to draw the graph
edge_labels = nx.get_edge_attributes(G, "weight") # get edge labels
pos = nx.spring_layout(G) # get position of nodes with a spring model layout
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels)

plt.axis("off")
plt.savefig('graph.png')
'''
def kruskal(G):
    ds = DisjointSet()
    sets_count = len(G.nodes)
    mst = []
    for n in G.nodes:
        ds.makeset(n)
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    for e in edges:
        s,t, _ = e
        ps, pt = map(ds.find, (s,t))
        if ps == pt:
            #components already connected, skip
            continue
        ds.union(s,t)
        mst.append(e)
        sets_count -= 1
        if sets_count == 1:
            return mst
    print("graph is not connected, failing")
    return





# load graphs and run functions

graph = pickle.load(open(args.graph,'rb'))
mst = kruskal(graph)
mst_edges = {(u,v) for (u,v,_) in mst}
other_edges = set(graph.edges) - mst_edges

edge_labels = nx.get_edge_attributes(graph, "weight") # get edge labels
pos = nx.spring_layout(graph, seed=12) # get position of nodes with a spring model layout
nx.draw_networkx_edges(graph, pos, edgelist=mst_edges, width=6)
nx.draw_networkx_edges(graph, pos, edgelist=other_edges, width=3)

nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos)
nx.draw_networkx_edge_labels(graph, pos, edge_labels)

plt.axis("off")
plt.tight_layout()
plt.savefig('mst.png')

