'''
COMP 5970/6970 Graph Algorithms Homework 7 coding section
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
import math
from collections import namedtuple, defaultdict

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement Dijkstras min path and A* search on the maze graph G to find the best
route from s to t. nodes are named with their coordinate position. 
Feel free to use the queue package
Report the number of nodes expanded (popped from the queue) as well
as touched (added to the queue)

use euclidean (or manhattan distance as it is on a grid graph) distance to t as your heuristic
'''
HeapNode = namedtuple('HeapNode', 'key value')

class IndexedPriorityQueue:
    def __init__(self):
        self.min_heap = []
        self.index = {}

    def push(self, key, value):
        to_add = HeapNode(key, value)
        new_idx = len(self.min_heap)
        self.index[key] = new_idx
        self.min_heap.append(to_add)
        self.__heapify_up(key)
        # your code here

    def popmin(self):
        last_item = self.min_heap.pop()
        if not self.min_heap:
            del self.index[last_item.key]
            return last_item
        
        to_yield = self.min_heap[0]
        self.min_heap[0] = last_item
        self.index[last_item.key] = 0

        self.__heapify_down(last_item.key)

        del self.index[to_yield.key]
        return to_yield

    def peek(self):
        return self.min_heap[0]

    def decrease_key(self, key, new_value):
        # because it's a decrease, we can only ever go up the min heap
        curr_idx = self.index[key]
        existing = self.min_heap[curr_idx]
        assert new_value <= existing.value
        self.min_heap[curr_idx] = HeapNode(key, new_value)
        self.__heapify_up(key)
    
    def __heapify_up(self, key):
        curr_idx = self.index[key]
        curr = self.min_heap[curr_idx]
        # if we're heapify-ing up, we should check if the parent is 
        # less than the value at the current node. If so, move parent down
        # continue until we can't move parent, then we place the curr at its destination
        
        # because of how we index, an odd number is a left child, and an even number is right child
        while curr_idx > 0:
            # this changes either 2i+1 or 2i+2 into 2i
            offset = (curr_idx % 2) - 2
            parent_idx = (curr_idx + offset) // 2
            parent = self.min_heap[parent_idx]

            if curr.value < parent.value:
                self.min_heap[curr_idx] = parent
                self.index[parent.key] = curr_idx
                curr_idx = parent_idx
            else:
                break
        self.min_heap[curr_idx] = curr
        self.index[curr.key] = curr_idx

    def __heapify_down(self, key):
        curr_idx = self.index[key]
        curr = self.min_heap[curr_idx]
        heap_len = len(self.min_heap)
        # if we're heapify-ing down, we should check if either child is 
        # less than the value at the current node. If so, move child to parent spot
        # then, continue going down trying to place the original
        l_child_idx = curr_idx*2 + 1
        r_child_idx = l_child_idx + 1

        while l_child_idx < heap_len:
            if self.min_heap[l_child_idx].value < curr.value: 
                # perfer taking right to maintain complete trees
                if r_child_idx < heap_len and self.min_heap[r_child_idx].value <= self.min_heap[l_child_idx].value:
                    right_key = self.min_heap[r_child_idx].key
                    self.index[right_key] = curr_idx
                    self.min_heap[curr_idx] = self.min_heap[r_child_idx]
                    curr_idx = r_child_idx
                else:
                    left_key = self.min_heap[l_child_idx].key
                    self.index[left_key] = curr_idx
                    self.min_heap[curr_idx] = self.min_heap[l_child_idx]
                    curr_idx = l_child_idx
            elif r_child_idx < heap_len and self.min_heap[r_child_idx].value < curr.value:
                right_key = self.min_heap[r_child_idx].key
                self.index[right_key] = curr_idx
                self.min_heap[curr_idx] = self.min_heap[r_child_idx]
                curr_idx = r_child_idx
            else:
                break
            l_child_idx = curr_idx*2 + 1
            r_child_idx = l_child_idx + 1
        self.index[key] = curr_idx
        self.min_heap[curr_idx] = curr

    def __len__(self):
        return len(self.min_heap)
    def __bool__(self):
        return bool(self.min_heap)
    def __getitem__(self, key):
        # will throw key error if bad
        idx = self.index[key]
        return self.min_heap[idx].value

def Dijkstra(G, s, t):
    ipq = IndexedPriorityQueue()
    finalized_dists = {}
    parents = {}
    expanded = 0
    touched = 0
    for node in G.nodes:
        ipq.push(node, math.inf)
        parents[node] = node
    ipq.decrease_key(s, 0)

    while ipq:
        key, value = ipq.popmin()
        expanded += 1
        finalized_dists[key] = value
        if key == t:
            break
        for neighbor in G.adj[key]:
            if neighbor in finalized_dists:
                continue
            touched += 1
            weight = 1
            possible_new_val = value + weight

            if possible_new_val < ipq[neighbor]:
                ipq.decrease_key(neighbor, possible_new_val)
                parents[neighbor] = key
    order_to_end = []
    curr = t
    while (curr != s):
        order_to_end.append(curr)
        curr = parents[curr]
    path = [s] + [*reversed(order_to_end)]
    # print(f"Dijkstra: Min path from {s} to {t} is {', '.join(map(str, path))}")
    print(f"Dijkstra: Min path from {s} to {t} has cost {len(path)}")
    print(f"Dijkstra {expanded=} {touched=}", end='\n\n') 


def Astar(G, s, t):
    def h(x):
        # return 0
        # return math.hypot(x[0]-t[0], x[1]-t[1])
        return abs(x[0]-t[0])  + abs(x[1]-t[1])

    ipq = IndexedPriorityQueue()
    curr_dists = {}
    finalized_dists = {}
    parents = {}
    expanded = 0
    touched = 0
    for node in G.nodes:
        ipq.push(node, math.inf)
        # touched += 1
        curr_dists[node] = math.inf
        parents[node] = node
    ipq.decrease_key(s, h(s))
    curr_dists[s] = 0

    while ipq:
        key, _ = ipq.popmin()
        expanded += 1
        value = curr_dists[key]
        finalized_dists[key] = value
        if key == t:
            break
            
        for neighbor in G.adj[key]:
            if neighbor in finalized_dists:
                continue
            touched += 1
            # weight = G[key][neighbor]['weight']
            weight = 1
            possible_new_val = value + weight

            if possible_new_val < curr_dists[neighbor]:
                ipq.decrease_key(neighbor, possible_new_val + h(neighbor))
                curr_dists[neighbor] = possible_new_val
                parents[neighbor] = key
    order_to_end = []
    curr = t
    while (curr != s):
        order_to_end.append(curr)
        curr = parents[curr]
    path = [s] + [*reversed(order_to_end)]
    # print(f"A*: Min path from {s} to {t} is {', '.join(map(str, path))}")
    print(f"A*: Min path from {s} to {t} has cost {len(path)}")
    print(f"A* {expanded=} {touched=}")




'''
Problem 2 Implement the louvain method for community detection on the Graph G. 
visualize the final graph colored by cluster

'''
def louvain(G):
    node_to_community = {v:i for i, v in enumerate(list(G.nodes))}
    community_to_nodes = {node_to_community[v]:{v} for v in node_to_community}
    
    def possible_modularity(G, moving_node, new_comm):
        old_comm = node_to_community[moving_node]
        community_to_nodes[old_comm].remove(v)
        community_to_nodes[new_comm].add(v)
        res = nx.community.modularity(G, community_to_nodes.values())
        community_to_nodes[old_comm].add(v)
        community_to_nodes[new_comm].remove(v)
        return res
    
    original_G = G.copy()
    start_nodes_to_cluster = {}
    iteration = 1
    any_change = True
    while any_change:
        while any_change:
            any_change = False
            for v in G.nodes:
                best_comm = None
                best_delta = 0
                start_modularity = nx.community.modularity(G, community_to_nodes.values())
                for x in G.adj[v]:
                    if node_to_community[x] != node_to_community[v]:
                        delta = possible_modularity(G, v, node_to_community[x]) - start_modularity
                        if delta > best_delta:
                            best_comm = node_to_community[x]
                            best_delta = delta
                if best_comm is not None:
                    any_change = True
                    old_comm = node_to_community[v]
                    community_to_nodes[old_comm].remove(v)
                    if len(community_to_nodes[old_comm]) == 0:
                        del community_to_nodes[old_comm]
                    node_to_community[v] = best_comm
                    community_to_nodes[best_comm].add(v)

        any_change = False
        if not start_nodes_to_cluster:
            # keep track for the first one
            start_nodes_to_cluster = {k:v for k, v in node_to_community.items()} 
        else:
            # start_nodes_to_cluster contains the results of the last one
            # the name of the contacted node in the new graph is one of the old ones
            # kinda like union find, it has a representative.
            new_start_nodes_to_cluster = {}
            for k, v in node_to_community.items():
                new_start_nodes_to_cluster[k] = v
            # if a key is not in the new one, look though existing keys
            # for each, see if it was in the same cluster in the step before. 
            # if so, take the new cluster value
            for oldkey in start_nodes_to_cluster:
                if oldkey not in new_start_nodes_to_cluster:
                    for newkey in new_start_nodes_to_cluster:
                        if start_nodes_to_cluster[newkey] == start_nodes_to_cluster[oldkey]:
                            new_start_nodes_to_cluster[oldkey] = new_start_nodes_to_cluster[newkey]
                            break
            start_nodes_to_cluster = new_start_nodes_to_cluster

        node_groups = defaultdict(set)
        for k,v in start_nodes_to_cluster.items():
            node_groups[v].add(k)
        node_groups = list(node_groups.values())

        print(f"After iteration {iteration}, clustering was")
        print(start_nodes_to_cluster, end="\n\n")
        # print(node_groups)
        plt.figure(iteration)
        pos = nx.spring_layout(original_G)
        colors = ['red', 'green', 'blue', 'orange', 'yellow', 'purple']
        for i, group in enumerate(node_groups):
            nx.draw_networkx_nodes(original_G, pos, nodelist=group, node_size=150, node_color=colors[i])
        nx.draw_networkx_edges(original_G, pos, width=0.3)
        nx.draw_networkx_labels(original_G, pos, font_color='w')
        plt.axis("off")
        plt.savefig(f'clustering_iter{iteration}.png')
        

        G_prime = nx.MultiGraph(G)
        for node_in_comm in community_to_nodes.values():
            to_contract = list(node_in_comm)
            start = to_contract[0]
            for node in to_contract[1:]:
                G_prime = nx.contracted_nodes(G_prime, start, node, self_loops=False)
        if not nx.is_isomorphic(G, G_prime) and len(G_prime.nodes) > 1:
            G = G_prime
            any_change = True
            node_to_community = {v:i for i, v in enumerate(list(G.nodes))}
            community_to_nodes = {node_to_community[v]:{v} for v in node_to_community}
            iteration += 1




# make graph and run functions
G = nx.grid_2d_graph(5,8)
G.remove_node((1,1))
G.remove_node((1,2))
G.remove_node((1,3))
G.remove_node((3,1))
G.remove_node((3,3))
G.remove_node((3,4))
G.remove_node((3,5))
G.remove_node((3,6))
G.remove_node((0,5))
G.remove_node((1,5))
'''
This graph should represent the following maze
_____
t    |
   x |
xx x |
   x |
 x x |
 x   |
 x x |
s    |
-----

'''
Dijkstra(G, (0,0), (0,7))
Astar(G, (0,0), (0,7))

G = nx.Graph()
G.add_nodes_from([x for x in "abcdefghijklmno"])
G.add_edges_from([("a","b"),("a","c"),("a","d"),("b","c"),("b","d"),("c","e"),("d","e")])
G.add_edges_from([("f","g"),("f","h"),("f","i"),("f","j"),("g","j"),("g","h"),("h","i"),("h","j"),("i","j")])
G.add_edges_from([("k","l"),("k","n"),("k","m"),("l","n"),("n","m"),("n","o"),("m","o")])
G.add_edges_from([("e","f"),("j","l"),("j","n")])

louvain(G)

