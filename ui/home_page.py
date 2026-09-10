"""
Educational dashboard overview and quick-navigation cards.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from visualization.styles import PALETTE

class HomePage(QWidget):
    def __init__(self, nav_callback, parent=None):
        super().__init__(parent)
        self.nav_callback = nav_callback
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Header
        header = QVBoxLayout()
        title = QLabel("Algorithm Visualizer")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet(f"color: {PALETTE['accent_blue']};")
        subtitle = QLabel("An interactive algorithm laboratory to strengthen data structure and algorithmic intuition.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Grid of Module Cards
        grid = QGridLayout()
        grid.setSpacing(16)

        modules = [
            ("Sorting Algorithms", "Observe comparison and partitioning in Bubble, Merge, Quick Sort.", 1),
            ("Searching Algorithms", "Linear vs logarithmic Binary Search over discrete arrays.", 2),
            ("Stack Visualizer", "LIFO (Last In, First Out) node pointer push and pop dynamics.", 3),
            ("Queue Visualizer", "FIFO node enqueue/dequeue and Circular Queue pointer wrap-around.", 4),
            ("Linked List", "Dynamic memory nodes, pointer reversals, and linear lookups.", 5),
            ("Binary Search Tree", "Hierarchical insertion comparisons, deletions, and recursive traversals.", 6),
            ("Graph Visualizer", "Adjacency lists, vertex discovery, and BFS / DFS traversal waves.", 7),
            ("Pathfinding / Maze", "Grid-as-graph state space exploration and optimal shortest path extraction.", 8),
            ("Algorithm Comparison", "Benchmarking comparisons and theoretical complexities side-by-side.", 9),
        ]

        for idx, (m_title, m_desc, nav_idx) in enumerate(modules):
            card = QFrame()
            card.setObjectName("card")
            card_layout = QVBoxLayout(card)

            t = QLabel(m_title)
            t.setFont(QFont("Segoe UI", 13, QFont.Bold))
            d = QLabel(m_desc)
            d.setWordWrap(True)
            d.setStyleSheet(f"color: {PALETTE['text_secondary']};")

            btn = QPushButton("Launch Module →")
            btn.setObjectName("action_btn")
            btn.clicked.connect(lambda _, n=nav_idx: self.nav_callback(n))

            card_layout.addWidget(t)
            card_layout.addWidget(d)
            card_layout.addStretch()
            card_layout.addWidget(btn)

            row, col = divmod(idx, 3)
            grid.addWidget(card, row, col)

        layout.addLayout(grid)

        # Topics Covered Section
        topics_card = QFrame()
        topics_card.setObjectName("card")
        topics_layout = QVBoxLayout(topics_card)
        t_label = QLabel("Curriculum & Topics Covered")
        t_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        t_items = QLabel(
            "• Linear Structures: Stack, Queue, Circular Queue, Singly Linked List\n"
            "• Non-Linear Structures: Binary Search Trees, Graph Adjacency Lists\n"
            "• Core Algorithms: Bubble, Selection, Insertion, Merge, Quick Sort\n"
            "• Traversals: BFS, DFS, Preorder, Inorder (produces sorted order), Postorder\n"
            "• Complexity Analysis: Best, Average, Worst Time Complexity & Auxiliary Space Complexity"
        )
        t_items.setStyleSheet(f"color: {PALETTE['text_secondary']}; line-height: 1.5;")
        topics_layout.addWidget(t_label)
        topics_layout.addWidget(t_items)
        layout.addWidget(topics_card)
        layout.addStretch()