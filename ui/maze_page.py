"""
Pathfinding / Maze Visualizer demonstrating BFS vs DFS exploration waves on a grid-as-graph.
"""
import random
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from algorithms.pathfinding import grid_bfs, grid_dfs
from visualization.maze_canvas import MazeCanvas
from visualization.styles import PALETTE

class MazePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.generator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.start_time = 0
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Breadth First Search (Guarantees Shortest Path)", "Depth First Search (Exploration Only)"])

        rand_btn = QPushButton("Generate Random Maze")
        rand_btn.clicked.connect(self._random_maze)

        clear_walls_btn = QPushButton("Clear Walls")
        clear_walls_btn.clicked.connect(self._clear_walls)

        start_btn = QPushButton("Find Path")
        start_btn.setObjectName("action_btn")
        start_btn.clicked.connect(self._start)

        step_btn = QPushButton("Next Step")
        step_btn.clicked.connect(self._step)

        reset_btn = QPushButton("Reset Search")
        reset_btn.clicked.connect(self._reset_search)

        ctrl_layout.addWidget(QLabel("Algorithm:"))
        ctrl_layout.addWidget(self.algo_combo)
        ctrl_layout.addWidget(rand_btn)
        ctrl_layout.addWidget(clear_walls_btn)
        ctrl_layout.addWidget(start_btn)
        ctrl_layout.addWidget(step_btn)
        ctrl_layout.addWidget(reset_btn)
        layout.addWidget(ctrl_card)

        self.canvas = MazeCanvas(rows=16, cols=16)
        layout.addWidget(self.canvas)

        # Telemetry
        self.telemetry = QFrame()
        self.telemetry.setObjectName("card")
        t_layout = QHBoxLayout(self.telemetry)
        self.explored_lbl = QLabel("Cells Explored: 0")
        self.path_lbl = QLabel("Path Length: 0")
        self.time_lbl = QLabel("Elapsed: 0.00s")
        self.status_lbl = QLabel("Click grid cells to add/remove barrier walls")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_blue']};")
        t_layout.addWidget(self.explored_lbl)
        t_layout.addWidget(self.path_lbl)
        t_layout.addWidget(self.time_lbl)
        t_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry)

    def _random_maze(self):
        self._reset_search()
        for r in range(self.canvas.rows):
            for c in range(self.canvas.cols):
                if (r, c) not in (self.canvas.start, self.canvas.goal):
                    self.canvas.grid[r][c] = 1 if random.random() < 0.28 else 0
        self.canvas.update()

    def _clear_walls(self):
        self._reset_search()
        self.canvas.grid = [[0 for _ in range(self.canvas.cols)] for _ in range(self.canvas.rows)]
        self.canvas.update()

    def _start(self):
        if self.generator is None:
            algo = self.algo_combo.currentText()
            fn = grid_bfs if "BFS" in algo else grid_dfs
            self.generator = fn(self.canvas.grid, self.canvas.start, self.canvas.goal)
            self.start_time = time.time()
        self.timer.start(25)

    def _step(self):
        if self.generator is None:
            self._start()
            return
        try:
            event = next(self.generator)
            self.canvas.explored = event.get('explored', [])
            self.canvas.path = event.get('path', [])
            self.canvas.current = event.get('current', None)
            self.canvas.update()

            self.explored_lbl.setText(f"Cells Explored: {len(self.canvas.explored)}")
            self.path_lbl.setText(f"Path Length: {len(self.canvas.path)}")
            self.time_lbl.setText(f"Elapsed: {(time.time() - self.start_time):.2f}s")
            self.status_lbl.setText(event.get('desc', ''))

            if event['type'] == 'finish':
                self.timer.stop()
        except StopIteration:
            self.timer.stop()

    def _reset_search(self):
        self.timer.stop()
        self.generator = None
        self.canvas.explored = []
        self.canvas.path = []
        self.canvas.current = None
        self.canvas.update()
        self.explored_lbl.setText("Cells Explored: 0")
        self.path_lbl.setText("Path Length: 0")
        self.time_lbl.setText("Elapsed: 0.00s")
        self.status_lbl.setText("Ready")