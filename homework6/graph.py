import networkx as nx
import matplotlib.pyplot as plt


G = nx.complete_graph(100)

import random
random.seed(4)



for (x,y) in G.edges:
    if random.random() > 0.1:
        G.remove_edge(x,y)




G2 = nx.complete_graph(100)

for (x,y) in G2.edges:
    print(x,y)
    if (x < 50 and y > 50) or (x > 50 and y < 50):
        if random.random() > 0.05:
            G2.remove_edge(x,y)
    else:
        if random.random() > 0.4:
            G2.remove_edge(x,y)

nx.drawing.nx_pydot.write_dot(G2, "graph.dot")


G = nx.MultiGraph(G)
