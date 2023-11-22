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
    fake_edges = []
    for u in left_nodes:
        for v in right_nodes:
            if not G.has_edge(u, v):
                fake_edges.append((u,v, {'weight': 0}))
                G.add_edge(u, v, weight=-int(1e9))
    print('Fake:', fake_edges)

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
        # print('matching', matching)
        # print('potentials', potentials)
        # if all((u in matching for u in left_nodes)):
        #     # we're done
        #     return matching
        
        def augment(visited, u):
            if u in visited:
                return False
            visited.add(u)
            for v, data in G[u].items():
                if potentials[u] + potentials[v] != data[weight]:
                    continue
                if v not in matching or augment(visited, matching[v]):
                    matching[v] = u
                    matching[u] = v
                    return True
            return False

        # find an unmatched left node
        for u in left_nodes:
            visited = set()
            if u not in matching and not augment(visited, u):
                cutset = set()
                for v in visited:
                    if v not in matching:
                        cutset.add(v)
                    else:
                        cutset.add(v)
                        cutset.add(matching[v])
                break
        else:
            # we're done
            return matching
        # print('matching after augment', matching)
        # print('cutset', cutset)


        # use augmenting path as cut set
        # adjust edges between the cut set and complement
        s = set(left_nodes).intersection(cutset)
        t = set(right_nodes).intersection(cutset)
        # print(s,t)
        min_delta = float('inf')
        for u,v,data in G.edges(data=True):
            if u in s and v not in t:
                possible = potentials[u] + potentials[v] - data[weight]
                # print(u,v,possible)
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
    random.seed(40)
    G = bipartite.random_graph(5, 3, 0.7)
    left_nodes = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
    right_nodes = {r for r in G.nodes() if r not in left_nodes}

    # available_weights = list(range(1, 50))
    # random.shuffle(available_weights)
    available_weights = [random.randint(1,9) for _ in range(len(G.edges))]
    idx = 0
    for u, v in G.edges():
        G[u][v]['weight'] = available_weights[idx]
        idx += 1
    # print(G.edges(data=True))

    print(G.edges(data=True))
    pos = nx.bipartite_layout(G, left_nodes)
    nx.draw_networkx(G, pos=pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, label_pos=0.8)
    # plt.show()

    def fmt_match(m):
        return {k: v for k, v in m.items() if k in left_nodes}

    max_match = hungarian(G)
    max_match = fmt_match(max_match)
    total_weight = 0
    for u, v in max_match.items():
        # don't count fake nodes
        if u in G.nodes() and v in G.nodes():
            total_weight += G[u][v]['weight']
    print(max_match, total_weight)

    H = G.copy()
    for u,v,d in H.edges(data=True):
        d['weight'] = -d['weight']
    min_match = nx.bipartite.minimum_weight_full_matching(H, top_nodes=left_nodes)
    min_match = fmt_match(min_match)
    total_weight = 0
    for u, v in min_match.items():
        if u in H.nodes() and v in H.nodes():
            total_weight -= H[u][v]['weight']
    print(min_match, total_weight)

    plt.show()