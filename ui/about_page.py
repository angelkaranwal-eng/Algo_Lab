"""
Educational application architecture and portfolio reference page.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QFont
from visualization.styles import PALETTE

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        title = QLabel("Algorithm Visualizer")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet(f"color: {PALETTE['accent_blue']};")

        subtitle = QLabel("An interactive educational application for understanding fundamental Data Structures and Algorithms through step-by-step visualization.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {PALETTE['text_secondary']};")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(12)

        sections = [
            ("Core Mission", "To demystify abstract data representations and algorithmic execution flows by converting in-memory pointer manipulations and comparisons into real-time visual step operations for interview and academic prep."),
            ("Custom Data Structures", "Node-based Stack, Node-based Queue, Array Circular Queue, Singly Linked List with manual pointer reversals, Binary Search Tree with full two-child deletion handling, and Adjacency List Graph representation."),
            ("Implemented Algorithms", "Sorting (Bubble, Selection, Insertion, Merge, Quick Sort), Searching (Linear, Binary Search), Graph Traversals (Breadth First Search, Depth First Search), Grid Pathfinding (BFS, DFS)."),
            ("Design Principles", "No games, scorebars, or simulated animations: visualizations consume yielded runtime telemetry generated directly by the underlying algorithms.")
        ]

        for h, body in sections:
            lbl_h = QLabel(h)
            lbl_h.setFont(QFont("Segoe UI", 11, QFont.Bold))
            lbl_b = QLabel(body)
            lbl_b.setWordWrap(True)
            lbl_b.setStyleSheet(f"color: {PALETTE['text_secondary']}; line-height: 1.4;")
            info_layout.addWidget(lbl_h)
            info_layout.addWidget(lbl_b)

        layout.addWidget(info_card)
        layout.addStretch()