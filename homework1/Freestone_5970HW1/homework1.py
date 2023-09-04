'''
COMP 5970/6970 Graph Algorithms Homework 1 coding section
requires networkx, argparse, and chess 
requires python 3.6+ (can get with anaconda or elsewhere, note standard python with mac is python 2)
pip install networkx
pip install argparse
pip install chess
'''

import argparse
import chess
import networkx as nx
import pickle
from collections import namedtuple, deque

parser = argparse.ArgumentParser()
parser.add_argument("--graph1", help="file containing graph in adjacency list format for problem 1")
parser.add_argument("--start_node1", help="name of start node for problem 1")
parser.add_argument("--end_node1", help="name of end node for problem 1")
parser.add_argument("--graph2", help="file containing graph in pickle format")
args = parser.parse_args()

'''
Problem 1
Traverses maze graph G (networkx Graph) in a DFS manner. You may make a helper function
for networkx graphs, you iterate over the adjacent nodes with
for neighbor in G[node_name]:

and you can store and access arbitrary information in nodes with 
G.nodes[node_name][attribute_name]

Keep track of the previous node in the path such that you can output the node path from start to end
node names are (x,y) denoting locations in the maze
outputs: prints path from start_node to end_node
'''
def maze(G, start_node: str, end_node: str):
    StackItem = namedtuple('StackItem', 'vertex path')
    stack = []
    stack.append(StackItem(start_node, path=tuple([start_node])))
    while stack:
        vertex, curr_path = stack.pop()
        node = G.nodes[vertex]
        if 'visited' in node:
            continue
        node['visited'] = True
        for adj in G[vertex]:
            new_path = curr_path+tuple([adj])
            if adj == end_node:
                print(', '.join(new_path))
                return
            new_item = StackItem(adj, path=new_path)
            stack.append(new_item)
    print("No path exists.")

'''
Problem 2
Traverse the chess move graph G (networkx Graph) in a BFS manner until you find the fastest checkmate
node names are a text representation of the state of the game including board position
you can print out the position with print(chess.Board(node_name))

node objects contain there parent node name accessed by G.nodes[node_name]['parent']
node objects contain the move that led to this position which is accessed by G.nodes[node_name]['move'] (this is None for the starting position)

you can check whether a position is checkmate via the following code
board = chess.Board(node_name)
if board.is_checkmate():
    #do something
    
outputs: prints move sequence to fastest possible checkmate
'''
def checkmate(G, start_node: str):
    if chess.Board(start_node).is_checkmate():
        print(G[start_node]['move'])

    queue = deque()
    queue.append(start_node)
    while queue:
        move = queue.popleft()
        node = G.nodes[move]
        if 'visited' in node:
            continue
        node['visited'] = True
        for adj in G[move]:
            if chess.Board(adj).is_checkmate():
                curr = adj
                moves = []
                while curr:
                    move = G.nodes[curr]['move']
                    if move: moves.append(move)
                    curr = G.nodes[curr]['parent']
                print(', '.join(reversed(moves)))
                return
            queue.append(adj)
    print("No path exists")

# load graphs and run functions
maze_graph = nx.read_adjlist(args.graph1)
maze(maze_graph, args.start_node1, args.end_node1)

chess_movetree = pickle.load(open(args.graph2,'rb'))
start_node = chess.Board().fen() # node name for the starting game position
checkmate(chess_movetree, start_node)


