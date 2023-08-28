from collections import deque
def bfs1(G,v):
    queue = deque()
    visited = set()
    queue.append(v)
    visited.add(v)
    while queue:
        curr = queue.popleft()
        print(f"BFS popped {curr}")
        for adj in G[curr]:
            if adj not in visited:
                queue.append(adj)
                visited.add(adj)


def bfs2(G,v):
    queue = deque()
    visited = set()
    queue.append(v)
    while queue:
        curr = queue.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        print(f"BFS popped {curr}")
        for adj in G[curr]:
            queue.append(adj)


