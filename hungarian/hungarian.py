import networkx as nx
from networkx.algorithms import bipartite
import random
import matplotlib.pyplot as plt
from collections import deque

def hungarian(inG, left_nodes=None, weight='weight'):
    if left_nodes is None:
        left_nodes = {n for n, d in inG.nodes(data=True) if d['bipartite'] == 0}
    else:
        left_nodes = set(left_nodes)
    if len(left_nodes) == 0:
        raise nx.NetworkXError("Graph is not bipartite")
    if not bipartite.is_bipartite(inG):
        raise nx.NetworkXError("Graph is not bipartite")
    if inG.is_multigraph():
        raise nx.NetworkXError("MultiGraph not supported.")

    right_nodes = {r for r in inG.nodes() if r not in left_nodes}
    G = inG.copy()
    if len(left_nodes) > len(right_nodes):
        # add fake nodes to make it square
        for i in range(len(left_nodes) - len(right_nodes)):
            nodename = 'FAKE_NODE_{}'.format(i)
            G.add_node(nodename, bipartite=1)
            right_nodes.add(nodename)

    # add fake edges to make it complete
    for u in left_nodes:
        for v in right_nodes:
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=-int(1e9))

    # Initialize dictionary of matching edges and potentials
    matching = {}
    potentials = {}

    # start potential values are the maximum edge weight for each left node
    for u in left_nodes:
        potentials[u] = max((d.get(weight, 1) for _, d in G[u].items()))
    # potentials for all right nodes is 0
    for v in right_nodes:
        potentials[v] = 0

    # match free vertices
    while True:
        print('matching', matching)
        print('potentials', potentials)
        if all((u in matching for u in left_nodes)):
            # we're done
            formatted_matching = {}
            for u, v in matching.items():
                if u in left_nodes:
                    formatted_matching[u] = v
            return formatted_matching

        queue = deque([u for u in left_nodes if u not in matching])
        previous = {u: None for u in queue}
        needs_potential_change = False
        while queue:
            u = queue.popleft()
            for _,v,data in G.edges(u, data=True):
                w = data[weight]
                if v not in previous and potentials[u] + potentials[v] == w:
                    if v in right_nodes:
                        previous[v] = u
                        break
                    else:
                        queue.append(matching[v])
                        queue.append(v)
                        previous[v] = u
        else:
            needs_potential_change = True

        if not needs_potential_change:
            matching.update({v:k for k,v in previous.items() if v is not None})
        print(previous)
        print('matching after', matching)
        # use augmenting path as cut set
        # adjust edges between the cut set and complement
        # cutset = set(augmenting_path)
        cutset = set(previous.keys())
        s = set(left_nodes).intersection(cutset)
        t = set(right_nodes).intersection(cutset)
        print(s,t)
        min_delta = float('inf')
        for u,v,data in G.edges(data=True):
            if u in s and v not in t:
                possible = potentials[u] + potentials[v] - data[weight]
                print(u,v,possible)
                min_delta = min(min_delta, possible)
        if min_delta == float('inf'):
            raise nx.NetworkXError("Min delta is inf")
        elif min_delta == 0:
            # we're done
            return matching

        # adjust potentials
        for u in s:
            potentials[u] -= min_delta
        for v in t:
            potentials[v] += min_delta
        # this is guaranteed to have made an other edge visible.
            
if __name__ == "__main__":
    G = bipartite.random_graph(3, 3, 1, seed=42)
    # add random weights
    #33

    random.seed(35)
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)
    print(G.edges(data=True))

    # pos = nx.bipartite_layout(G, [0, 1, 2])
    # nx.draw_networkx(G, pos=pos)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, label_pos=0.8)
    # plt.show()

    matching = hungarian(G)
    print(matching)
