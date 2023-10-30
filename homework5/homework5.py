'''
COMP 5970/6970 Graph Algorithms Homework 5 coding section
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
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Construct a de Bruijn graph with k=4 for the given sequence
Also save a picture of that graph
remember this is a directed graph, so you will want to use nx.DiGraph not nx.Graph
'''
def debruijn(sequence,k=4):
    G = nx.DiGraph()
    kmers = []
    for i in range(len(sequence)-k+1):
        kmers.append(sequence[i:i+k])
    for k1 in kmers:
        for k2 in kmers:
            if k1 == k2:
                continue
            if k1[1:] == k2[:-1]:
                if k1[:-1] not in G.nodes:
                    G.add_node(k1[:-1])
                if k2[1:] not in G.nodes:
                    G.add_node(k2[1:])
                if k1[1:] not in G.nodes:
                    G.add_node(k1[1:])
                G.add_edge(k1[:-1], k1[1:], label=k1)
                G.add_edge(k2[:-1], k2[1:], label=k1)

    
    edge_labels = nx.get_edge_attributes(G, "label")
    pos = nx.spring_layout(G, k = 6, seed=2)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos)
    # nx.draw_networkx_labels(G,pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.axis("off")
    plt.savefig('graph.png')

    return G
    # your code here



'''
Problem 2
Tarjan's algorithm for strongly connected components
helper functions are fine
'''
def tarjans(G):
    # your code here
    node_index_so_far = [0]
    stack = []
    on_stack = set()
    index = {}
    low_link = {}
    visited = set()
    sccs = []

    def strong_connect(v):
        index[v] = node_index_so_far[0]
        low_link[v] = node_index_so_far[0]
        # python mutability is funny.
        node_index_so_far[0] += 1
        stack.append(v)
        on_stack.add(v)
        visited.add(v)
        for x in G.adj[v]:
            if x not in visited:
                strong_connect(x)
            if x in on_stack:
                low_link[v] = min(low_link[v], low_link[x])
        if low_link[v] == index[v]:
            scc = []
            x = stack.pop()
            on_stack.remove(x)
            scc.append(x)
            while x != v:
                x = stack.pop()
                on_stack.remove(x)
                scc.append(x)
            sccs.append(scc)

    for n in G.nodes:
        if n not in visited:
            strong_connect(n)
    return sccs


'''
Problem 3
Code to tell whether a Eularian trail exists, and if it does, return the source node
Hint: you will want to make an edge between the sink node and source node, then
run Tarjan's algorithm on that Graph to ensure every node is reachable from the source
'''
def eularian_trail_exists(G):
    # confirm that the degrees are right
    source, sink = None, None
    for node in G.nodes:
        if G.in_degree(node) != G.out_degree(node):
            if G.out_degree(node) == G.in_degree(node) + 1:
                if not source:
                    source = node
                else:
                    return False
            if G.in_degree(node) == G.out_degree(node) + 1:
                if not sink:
                    sink = node
                else:
                    return False
    if not (source or sink) or (source and sink):
        # we might have more than one cc, check for that 
        # be sure to add an edge from sink to source, if one doenst exist
        if source or sink:
            G.add_edge(sink, source, label="FAKE EDGE")
        sccs = tarjans(G)
        if len(sccs) != 1:
            return False
        if source or sink:
            G.remove_edge(sink, source)
        return (source,sink,True)
    return False


'''
Problem 4: Find an Eularian trail through the de Bruijn graph of a sequence
using the Hierholzer algorithm and your previous code
Print out the sequence that that path represents
'''
def eularian_trail(sequence, k=4):
    G = debruijn(sequence, k=k)
    exist_check = eularian_trail_exists(G)
    if not exist_check:
        print("No valid Eulerian trail exists!")
        return
    source, _, _ = exist_check

    out_degs = {n:G.out_degree(n) for n in G.nodes}
    current_node = list(G.nodes)[0]
    if source:
        current_node = source
    trail = []
    dfs_stack = []
    dfs_stack.append(current_node)
    while dfs_stack:
        current_node = dfs_stack.pop()
        if out_degs[current_node] > 0:
            dfs_stack.append(current_node)
            next_node = list(G.adj[current_node])[-1]
            dfs_stack.append(next_node)
            G.remove_edge(current_node, next_node)
            out_degs[current_node] -=1
        else:
            trail.append(current_node)
    # its a stack, so reverse it. For a normal algorithm, we'd return that value
    trail = [*reversed(trail)]
    # instead, let's find the sequence it represents
    # each vertex is a (k-1)mer, so taking the first letter of all,
    # then tacking on last one, should reconstruct
    end_res = []
    for k1mer in trail[:-1]:
        end_res.append(k1mer[0]) 
    for c in trail[-1]:
        end_res.append(c)
    # for reference, the below line will print the input sequence and align it.
    # print(f"Input Sequence:\t\t{sequence}")
    print(f"Computed Sequence:\t{''.join(end_res)}")


    


# note that with k=5, you actually get the right answer!
eularian_trail("AAAGGCGTTGAGGTTT", k=4)

