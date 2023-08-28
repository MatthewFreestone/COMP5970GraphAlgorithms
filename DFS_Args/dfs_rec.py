def dfs_r(G, v, visited=set()):
    print(f"DFS called with {v}")
    visited.add(v)
    for adj in reversed(G[v]):
        if adj not in visited:
            dfs_r(G,adj, visited)
    


