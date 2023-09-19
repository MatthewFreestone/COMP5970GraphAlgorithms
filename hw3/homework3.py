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

import math
# this is a convenience class, does not provide any functionality that a min heap does
from collections import namedtuple

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement the indexed priority queue data structure backed by a list based min-heap 
and a dict based index.
Hint: if you store a binary tree in a vector with each new element being the final
element in the vector representing the last leaf node at the deepest level, you can
compute the index of the children of the node at position i as 2i+1 and 2i+2
You cannot import Queue or any other package for this problem.
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




'''
Problem 2
Dijkstras minimum path from s to t
You should use the Indexed priority queue from problem 1
'''
def Dijkstras(G, s, t):
    ipq = IndexedPriorityQueue()
    finalized_dists = {}
    parents = {}
    for node in G.nodes:
        ipq.push(node, math.inf)
        parents[node] = node
    ipq.decrease_key(s, 0)

    while ipq:
        key, value = ipq.popmin()
        finalized_dists[key] = value
        for neighbor in G.adj[key]:
            if neighbor in finalized_dists:
                continue
            weight = G[key][neighbor]['weight']
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
    print(f"Min path from {s} to {t} is {', '.join(map(str, path))}")
        


# make graph and run functions

G = nx.Graph()
G.add_nodes_from([x for x in "abcdef"])
G.add_edge("a","b", weight=14)
G.add_edge("a","c", weight=9)
G.add_edge("a","d", weight=7)
G.add_edge("b","c", weight=2)
G.add_edge("b","e", weight=9)
G.add_edge("c","d", weight=10)
G.add_edge("c","f", weight=11)
G.add_edge("d","f", weight=15)
G.add_edge("e","f", weight=6)
Dijkstras(G, "a", "e")
