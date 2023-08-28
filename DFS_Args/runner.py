from dfs_iter import dfs1, dfs2
from bfs_iter import bfs1, bfs2
from dfs_rec import dfs_r
G = {
        'a':['d','c','b'],
        'b':['d'],
        'c':[],
        'd':['e'],
        'e':[]
        }

print("Recurrsive DFS")
dfs_r(G,'a')
print("\nDFS with visiting on stack push")
dfs1(G,'a')
print("DFS with visiting on stack pop")
dfs2(G,'a')

print("\nBFS with visiting on queue enquque")
bfs1(G,'a')
print("\nBFS with visiting on queue dequeue")
bfs2(G,'a')


