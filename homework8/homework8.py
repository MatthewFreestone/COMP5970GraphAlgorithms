'''
COMP 5970/6970 Graph Algorithms Homework 8 coding section
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
from heapq import heappush, heappop
from dataclasses import dataclass, field
# import queue # use heapq instead, it is faster

parser = argparse.ArgumentParser()
args = parser.parse_args() # no arguments but im leaving this here

'''
Problem 1
Implement a ball-tree datastructure for fast knn_search
The data has just 2 dimensions, each row is a datapoint
'''
class BallTree:
    @dataclass
    class Node:
        left: 'BallTree.Node' = None
        right: 'BallTree.Node' = None
        center: np.ndarray = None
        radius: int = None
        leaf: bool = False
        def __init__(self, center, radius, leaf=False):
            self.left = None
            self.right = None
            self.center = center
            self.radius = radius
            self.leaf = leaf

    def __init__(self, data):
        self.root = self._create(data)

    def _create(self, data):
        if len(data) == 1:
            B = BallTree.Node(data[0], 0, leaf=True)
            return B
        else:
            range_x = np.max(data[:,0]) - np.min(data[:,0])
            range_y = np.max(data[:,1]) - np.min(data[:,1])
            d = 0 if range_x > range_y else 1
            c = np.median(data[:,d])
            left = data[data[:,d] < c]
            right = data[data[:,d] >= c]

            center = np.mean(data, axis=0)
            radius = np.max(np.linalg.norm(data - center, axis=1))
            B = BallTree.Node(center, radius)
            B.left = self._create(left)
            B.right = self._create(right)
            return B
'''
Problem 2 
implement knn_search on a balltree for a target point t and returning the k closest points
'''
@dataclass
class QNode:
    distance: int
    item: np.ndarray=field(compare=False)
    def __lt__(self, other):
        # use > to make it a max heap
        return self.distance > other.distance

def knn_search(B: BallTree.Node, t: np.ndarray, k: int, Q: list = []):
    if len(Q) == k and np.linalg.norm(t - B.center) - B.radius > Q[0].distance:
        return [q.item.center for q in Q]
    elif B.leaf:
        dist = np.linalg.norm(t - B.center)
        if len(Q) == 0 or dist < Q[0].distance:
            heappush(Q, QNode(dist, B))
            if len(Q) > k:
                heappop(Q)
    else:
        left_dist = np.linalg.norm(t - B.left.center)
        right_dist = np.linalg.norm(t - B.right.center)
        if left_dist < right_dist:
            knn_search(B.left, t, k, Q)
            knn_search(B.right, t, k, Q)
        else:
            knn_search(B.right, t, k, Q)
            knn_search(B.left, t, k, Q)
    return [q.item.center for q in Q]
    


'''
Problem 3
create a knn graph and output to a dot file
and visualize this in Gephi with force-atlas-2 or some other layout if you prefer
if you use the queue.PriorityQueue, you will want a class to store the priority and the data point
this will look like 
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
'''
def create_knn_graph(B, data, k):
    print("create knn graph and output dot file")
    for d in data:
        print
    # for each data point, find its k nearest neighbors and make edges in a graph to them
    # you will use your knn_search function to do this
    # you will need a max heap and can either use your code from a previous
    # homework or the queue.PriorityQueue (but this is min-heap so make sure to 
    # use the negative of the distance to make it a max heap)



data = np.loadtxt("data.csv",delimiter=",")
tree = BallTree(data)

res = knn_search(tree.root, np.array([0,0]), 10)
print(res)
# create_knn_graph(tree, data, 5)
