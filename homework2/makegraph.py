import pickle

import networkx as nx

import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from([x for x in "ABCDEFGHIJ"])

G.add_edge("A","B", weight = 5)
G.add_edge("A","E", weight = 1)
G.add_edge("A","D", weight = 4)
G.add_edge("B","D", weight = 2)
G.add_edge("B","C", weight = 4)
G.add_edge("C","J", weight = 2)
G.add_edge("C","I", weight = 1)
G.add_edge("C","H", weight = 1)
G.add_edge("J","I", weight = 0)
G.add_edge("I","H", weight = 6)
G.add_edge("I","G", weight = 4)
G.add_edge("G","H", weight = 1)
G.add_edge("G","D", weight = 11)
G.add_edge("H","D", weight = 2)
G.add_edge("G","F", weight = 7)
G.add_edge("F","D", weight = 5)
G.add_edge("F","E", weight = 1)
G.add_edge("E","D", weight = 2)

edge_labels = nx.get_edge_attributes(G, "weight")



pos = nx.spring_layout(G)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G,pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels)

plt.axis("off")
plt.savefig('graph.png')

pickle.dump(G, open("graph.pickle",'wb'))
