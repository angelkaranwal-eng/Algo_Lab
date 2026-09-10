"""
Graph Traversal Algorithms: BFS and DFS using manual queue and stack abstractions.
"""
from data_structures.queue import NodeBasedQueue
from data_structures.stack import NodeBasedStack

def bfs_traversal(graph, start_vertex: str):
    if start_vertex not in graph.adj_list:
        return

    visited = set()
    queue = [start_vertex]  # Auxiliary list for graph label representation
    visited.add(start_vertex)
    order = []

    yield {
        'type': 'start',
        'current': start_vertex,
        'visited': list(visited),
        'order': list(order),
        'frontier': list(queue),
        'desc': f"BFS initialized at vertex {start_vertex}"
    }

    while queue:
        curr = queue.pop(0)
        order.append(curr)
        yield {
            'type': 'process',
            'current': curr,
            'visited': list(visited),
            'order': list(order),
            'frontier': list(queue),
            'desc': f"Dequeued and visiting vertex {curr}"
        }

        for neighbor in sorted(graph.adj_list.get(curr, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                yield {
                    'type': 'discover',
                    'current': curr,
                    'neighbor': neighbor,
                    'visited': list(visited),
                    'order': list(order),
                    'frontier': list(queue),
                    'desc': f"Discovered unvisited neighbor {neighbor} -> Enqueued"
                }

    yield {
        'type': 'done',
        'current': None,
        'visited': list(visited),
        'order': list(order),
        'frontier': [],
        'desc': "BFS Traversal complete."
    }


def dfs_traversal(graph, start_vertex: str):
    if start_vertex not in graph.adj_list:
        return

    visited = set()
    stack = [start_vertex]
    order = []

    yield {
        'type': 'start',
        'current': start_vertex,
        'visited': list(visited),
        'order': list(order),
        'frontier': list(stack),
        'desc': f"DFS initialized at vertex {start_vertex}"
    }

    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            order.append(curr)
            yield {
                'type': 'process',
                'current': curr,
                'visited': list(visited),
                'order': list(order),
                'frontier': list(stack),
                'desc': f"Popped and visiting vertex {curr}"
            }

            for neighbor in sorted(graph.adj_list.get(curr, []), reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
                    yield {
                        'type': 'discover',
                        'current': curr,
                        'neighbor': neighbor,
                        'visited': list(visited),
                        'order': list(order),
                        'frontier': list(stack),
                        'desc': f"Pushed neighbor {neighbor} onto DFS stack"
                    }

    yield {
        'type': 'done',
        'current': None,
        'visited': list(visited),
        'order': list(order),
        'frontier': [],
        'desc': "DFS Traversal complete."
    }