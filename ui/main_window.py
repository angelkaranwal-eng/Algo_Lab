"""
Main window shell integrating dark dashboard theme, sidebar navigation, and stacked viewports.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from visualization.styles import PALETTE
from ui.home_page import HomePage
from ui.sorting_page import SortingPage
from ui.searching_page import SearchingPage
from ui.stack_page import StackPage
from ui.queue_page import QueuePage
from ui.linked_list_page import LinkedListPage
from ui.tree_page import TreePage
from ui.graph_page import GraphPage
from ui.maze_page import MazePage
from ui.comparison_page import ComparisonPage
from ui.about_page import AboutPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algorithm Visualizer - Laboratory & Learning System")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 700)
        self._buttons = []
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar Frame
        sidebar = QFrame()
        sidebar.setStyleSheet(f"background-color: {PALETTE['bg_card']}; border-right: 1px solid {PALETTE['border']};")
        sidebar.setFixedWidth(230)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(12, 18, 12, 18)
        side_layout.setSpacing(6)

        # App Brand Header
        brand_lbl = QLabel("ALGO LAB")
        brand_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        brand_lbl.setStyleSheet(f"color: {PALETTE['accent_blue']}; padding-left: 8px; margin-bottom: 12px;")
        side_layout.addWidget(brand_lbl)

        # Stacked Pages
        self.stack = QStackedWidget()
        self.pages = [
            HomePage(self.switch_page),
            SortingPage(),
            SearchingPage(),
            StackPage(),
            QueuePage(),
            LinkedListPage(),
            TreePage(),
            GraphPage(),
            MazePage(),
            ComparisonPage(),
            AboutPage()
        ]

        nav_items = [
            "Home", "Sorting", "Searching", "Stack", "Queue",
            "Linked List", "Binary Search Tree", "Graph", "Pathfinding",
            "Algorithm Comparison", "About"
        ]

        for idx, (label, page) in enumerate(zip(nav_items, self.pages)):
            self.stack.addWidget(page)
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 8px 12px;
                    border: none;
                    border-radius: 6px;
                    font-weight: 500;
                }}
                QPushButton:checked {{
                    background-color: {PALETTE['bg_card_secondary']};
                    color: {PALETTE['accent_blue']};
                    font-weight: bold;
                    border-left: 3px solid {PALETTE['accent_blue']};
                }}
            """)
            btn.clicked.connect(lambda _, i=idx: self.switch_page(i))
            side_layout.addWidget(btn)
            self._buttons.append(btn)

        side_layout.addStretch()
        self._buttons[0].setChecked(True)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    def switch_page(self, index: int):
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
            self._buttons[index].setChecked(True)