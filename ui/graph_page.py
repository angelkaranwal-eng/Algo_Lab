"""
Graph Visualizer with Adjacency List panel and BFS / DFS traversals.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QFrame, QMessageBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from data_structures.graph import Graph
from algorithms.graph_algorithms import bfs_traversal, dfs_traversal
from visualization.graph_canvas import GraphCanvas
from visualization.styles import PALETTE

class GraphPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = Graph(directed=False)
        self.generator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self._init_ui()
        self._seed_default_graph()

    def _seed_default_graph(self):
        for v in ['A', 'B', 'C', 'D', 'E']:
            self.graph.add_vertex(v)
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('A', 'C')
        self.graph.add_edge('B', 'D')
        self.graph.add_edge('C', 'E')
        self.graph.add_edge('D', 'E')
        self._refresh()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Control Panel
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.v_input = QLineEdit()
        self.v_input.setPlaceholderText("Vertex (e.g. F)")
        self.v_input.setMaximumWidth(100)

        add_v_btn = QPushButton("Add Vertex")
        add_v_btn.clicked.connect(self._add_vertex)

        self.u_input = QLineEdit()
        self.u_input.setPlaceholderText("From (A)")
        self.u_input.setMaximumWidth(70)
        self.v2_input = QLineEdit()
        self.v2_input.setPlaceholderText("To (B)")
        self.v2_input.setMaximumWidth(70)

        add_e_btn = QPushButton("Add Edge")
        add_e_btn.clicked.connect(self._add_edge)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Breadth First Search (BFS)", "Depth First Search (DFS)"])

        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Start (A)")
        self.start_input.setText("A")
        self.start_input.setMaximumWidth(80)

        traverse_btn = QPushButton("Start Traversal")
        traverse_btn.setObjectName("action_btn")
        traverse_btn.clicked.connect(self._start_traversal)

        step_btn = QPushButton("Next Step")
        step_btn.clicked.connect(self._step)

        reset_btn = QPushButton("Reset Graph")
        reset_btn.clicked.connect(self._seed_default_graph)

        ctrl_layout.addWidget(self.v_input)
        ctrl_layout.addWidget(add_v_btn)
        ctrl_layout.addWidget(self.u_input)
        ctrl_layout.addWidget(self.v2_input)
        ctrl_layout.addWidget(add_e_btn)
        ctrl_layout.addWidget(self.algo_combo)
        ctrl_layout.addWidget(self.start_input)
        ctrl_layout.addWidget(traverse_btn)
        ctrl_layout.addWidget(step_btn)
        ctrl_layout.addWidget(reset_btn)
        layout.addWidget(ctrl_card)

        # Body: Left = Canvas, Right = Adjacency Panel
        body_layout = QHBoxLayout()
        self.canvas = GraphCanvas()
        body_layout.addWidget(self.canvas, 7)

        adj_card = QFrame()
        adj_card.setObjectName("card")
        adj_layout = QVBoxLayout(adj_card)
        adj_title = QLabel("Adjacency List Structure")
        adj_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.adj_display = QTextEdit()
        self.adj_display.setReadOnly(True)
        self.adj_display.setStyleSheet(f"background-color: {PALETTE['bg_primary']}; border: 1px solid {PALETTE['border']};")
        adj_layout.addWidget(adj_title)
        adj_layout.addWidget(self.adj_display)
        body_layout.addWidget(adj_card, 3)

        layout.addLayout(body_layout)

        # Status & Complexity
        self.telemetry = QFrame()
        self.telemetry.setObjectName("card")
        t_layout = QHBoxLayout(self.telemetry)
        self.stats_lbl = QLabel("Vertices: 0 | Edges: 0")
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_green']};")
        t_layout.addWidget(self.stats_lbl)
        t_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry)

    def _add_vertex(self):
        v = self.v_input.text()
        if not self.graph.add_vertex(v):
            QMessageBox.warning(self, "Invalid Vertex", "Vertex label empty or already exists!")
            return
        self.v_input.clear()
        self._refresh()

    def _add_edge(self):
        u = self.u_input.text()
        v = self.v2_input.text()
        if not self.graph.add_edge(u, v):
            QMessageBox.warning(self, "Invalid Edge", "One or both vertex labels do not exist in graph!")
            return
        self._refresh()

    def _start_traversal(self):
        start_v = self.start_input.text().strip().upper()
        if start_v not in self.graph.adj_list:
            QMessageBox.warning(self, "Invalid Root", f"Starting vertex {start_v} not found!")
            return
        algo = self.algo_combo.currentText()
        self.generator = bfs_traversal(self.graph, start_v) if "BFS" in algo else dfs_traversal(self.graph, start_v)
        self.timer.start(400)

    def _step(self):
        if self.generator is None:
            self._start_traversal()
            return
        try:
            event = next(self.generator)
            self.canvas.set_graph(self.graph, active_vertex=event.get('current'), visited_vertices=set(event.get('visited', [])))
            self.status_lbl.setText(f"Order: {' → '.join(event.get('order', []))} | {event.get('desc')}")
            if event['type'] == 'done':
                self.timer.stop()
        except StopIteration:
            self.timer.stop()

    def _refresh(self):
        self.canvas.set_graph(self.graph)
        lines = []
        for v in self.graph.get_vertices():
            nbrs = ", ".join(self.graph.get_neighbors(v)) or "Ø"
            lines.append(f"{v} → [ {nbrs} ]")
        self.adj_display.setText("\n".join(lines))
        self.stats_lbl.setText(f"Vertices: {self.graph.vertex_count()} | Edges: {self.graph.edge_count()}")