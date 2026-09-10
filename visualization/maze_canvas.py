"""
Maze Grid Visualizer rendering traversable cells, obstacles, exploration wavefront, and paths.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt
from visualization.styles import PALETTE

class MazeCanvas(QWidget):
    def __init__(self, rows=15, cols=15, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)
        self.explored = []
        self.path = []
        self.current = None
        self.setMinimumSize(320, 320)

    def mousePressEvent(self, event):
        rect = self.rect()
        cell_w = rect.width() / self.cols
        cell_h = rect.height() / self.rows
        c = int(event.position().x() // cell_w)
        r = int(event.position().y() // cell_h)

        if 0 <= r < self.rows and 0 <= c < self.cols:
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = 1 if self.grid[r][c] == 0 else 0
                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        cell_w = rect.width() / self.cols
        cell_h = rect.height() / self.rows

        explored_set = set(self.explored)
        path_set = set(self.path)

        for r in range(self.rows):
            for c in range(self.cols):
                coord = (r, c)
                x = int(c * cell_w)
                y = int(r * cell_h)
                w = int(cell_w)
                h = int(cell_h)

                if coord == self.start:
                    color = QColor(PALETTE['accent_green'])
                elif coord == self.goal:
                    color = QColor(PALETTE['accent_red'])
                elif coord == self.current:
                    color = QColor(PALETTE['highlight'])
                elif coord in path_set:
                    color = QColor(PALETTE['accent_orange'])
                elif self.grid[r][c] == 1:
                    color = QColor(PALETTE['bg_card_secondary'])  # Wall
                elif coord in explored_set:
                    color = QColor('#1F3A5F')  # Explored wavefront
                else:
                    color = QColor(PALETTE['bg_card'])

                painter.fillRect(x, y, w, h, color)
                painter.setPen(QPen(QColor(PALETTE['border']), 1))
                painter.drawRect(x, y, w, h)