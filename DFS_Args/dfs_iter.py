def dfs1(G,v):
    stack = []
    visited = set()
    stack.append(v)
    visited.add(v)
    while stack:
        curr = stack.pop()
        print(f"DFS popped {curr}")
        for adj in G[curr]:
            if adj not in visited:
                stack.append(adj)
                visited.add(adj)


def dfs2(G,v):
    stack = []
    visited = set()
    stack.append(v)
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        print(f"DFS popped {curr}")
        for adj in G[curr]:
            stack.append(adj)


