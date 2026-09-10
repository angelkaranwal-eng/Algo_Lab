"""
Custom Graph representation using manual Adjacency List.
Nodes represent vertices; edges represent directed/undirected adjacencies.
"""

class Graph:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj_list = {}  # vertex_label -> list of neighbor labels

    def add_vertex(self, vertex: str) -> bool:
        vertex = vertex.strip().upper()
        if not vertex or vertex in self.adj_list:
            return False
        self.adj_list[vertex] = []
        return True

    def remove_vertex(self, vertex: str) -> bool:
        vertex = vertex.strip().upper()
        if vertex not in self.adj_list:
            return False
        del self.adj_list[vertex]
        for v in self.adj_list:
            if vertex in self.adj_list[v]:
                self.adj_list[v].remove(vertex)
        return True

    def add_edge(self, u: str, v: str) -> bool:
        u, v = u.strip().upper(), v.strip().upper()
        if u not in self.adj_list or v not in self.adj_list:
            return False
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if not self.directed:
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)
        return True

    def remove_edge(self, u: str, v: str) -> bool:
        u, v = u.strip().upper(), v.strip().upper()
        if u not in self.adj_list or v not in self.adj_list:
            return False
        if v in self.adj_list[u]:
            self.adj_list[u].remove(v)
        if not self.directed:
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)
        return True

    def get_vertices(self):
        return sorted(list(self.adj_list.keys()))

    def get_neighbors(self, vertex: str):
        return self.adj_list.get(vertex, [])

    def vertex_count(self) -> int:
        return len(self.adj_list)

    def edge_count(self) -> int:
        count = sum(len(neighbors) for neighbors in self.adj_list.values())
        return count if self.directed else count // 2

    def clear(self):
        self.adj_list.clear()

    def get_adjacency_matrix(self):
        vertices = self.get_vertices()
        v_idx = {v: i for i, v in enumerate(vertices)}
        matrix = [[0] * len(vertices) for _ in range(len(vertices))]
        for u in vertices:
            for v in self.adj_list[u]:
                matrix[v_idx[u]][v_idx[v]] = 1
        return vertices, matrix