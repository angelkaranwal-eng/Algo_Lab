"""
Grid Pathfinding Algorithms (BFS and DFS).
Models the 2D grid strictly as an implicit graph where each traversable cell is a vertex.
"""

def grid_bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = [start]
    visited = {start: None}
    explored = []

    yield {
        'type': 'step',
        'current': start,
        'explored': list(explored),
        'path': [],
        'desc': f"BFS started at root coordinate {start}"
    }

    found = False
    while queue:
        curr = queue.pop(0)
        explored.append(curr)
        yield {
            'type': 'explore',
            'current': curr,
            'explored': list(explored),
            'path': [],
            'desc': f"Exploring cell {curr}"
        }

        if curr == goal:
            found = True
            break

        r, c = curr
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 0 and neighbor not in visited:
                    visited[neighbor] = curr
                    queue.append(neighbor)

    path = []
    if found:
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = visited[curr]
        path.reverse()

    yield {
        'type': 'finish',
        'found': found,
        'current': goal if found else None,
        'explored': list(explored),
        'path': path,
        'desc': f"Pathfinding complete. {'Path discovered!' if found else 'No path exists.'}"
    }


def grid_dfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    visited = {start: None}
    explored = []

    yield {
        'type': 'step',
        'current': start,
        'explored': list(explored),
        'path': [],
        'desc': f"DFS started at root coordinate {start}"
    }

    found = False
    while stack:
        curr = stack.pop()
        if curr not in explored:
            explored.append(curr)
            yield {
                'type': 'explore',
                'current': curr,
                'explored': list(explored),
                'path': [],
                'desc': f"DFS visiting cell {curr}"
            }

            if curr == goal:
                found = True
                break

            r, c = curr
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                neighbor = (nr, nc)
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == 0 and neighbor not in visited:
                        visited[neighbor] = curr
                        stack.append(neighbor)

    path = []
    if found:
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = visited[curr]
        path.reverse()

    yield {
        'type': 'finish',
        'found': found,
        'current': goal if found else None,
        'explored': list(explored),
        'path': path,
        'desc': f"Pathfinding complete. {'Path discovered!' if found else 'No path exists.'}"
    }