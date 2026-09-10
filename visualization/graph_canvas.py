"""
Interactive Graph visualizer supporting visual vertex positioning and edge rendering.
"""
import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt, QPoint
from visualization.styles import PALETTE

class GraphCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = None
        self.positions = {}
        self.active_vertex = None
        self.visited_vertices = set()
        self.selected_vertex = None
        self.setMinimumHeight(340)

    def set_graph(self, graph, active_vertex=None, visited_vertices=None):
        self.graph = graph
        self.active_vertex = active_vertex
        self.visited_vertices = visited_vertices or set()
        self._calculate_default_positions()
        self.update()

    def _calculate_default_positions(self):
        if not self.graph:
            return
        vertices = self.graph.get_vertices()
        n = len(vertices)
        if n == 0:
            return

        rect = self.rect()
        cx, cy = rect.width() / 2, rect.height() / 2
        radius = min(cx, cy) - 50

        for i, v in enumerate(vertices):
            if v not in self.positions:
                angle = 2 * math.pi * i / n
                self.positions[v] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))

    def mousePressEvent(self, event):
        if not self.graph:
            return
        click_pos = event.pos()
        clicked_v = None
        for v, (x, y) in self.positions.items():
            if (click_pos.x() - x) ** 2 + (click_pos.y() - y) ** 2 <= 22 ** 2:
                clicked_v = v
                break

        if clicked_v:
            self.selected_vertex = clicked_v
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor(PALETTE['bg_card']))

        if not self.graph or self.graph.vertex_count() == 0:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(rect, Qt.AlignCenter, "Add vertices and edges to construct a custom graph")
            return

        # Draw edges
        painter.setPen(QPen(QColor(PALETTE['border']), 2))
        drawn_edges = set()
        for u, neighbors in self.graph.adj_list.items():
            if u not in self.positions:
                continue
            x1, y1 = self.positions[u]
            for v in neighbors:
                if v not in self.positions:
                    continue
                edge = tuple(sorted([u, v]))
                if not self.graph.directed and edge in drawn_edges:
                    continue
                drawn_edges.add(edge)
                x2, y2 = self.positions[v]
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Draw vertices
        r = 20
        for v, (x, y) in self.positions.items():
            if v == self.active_vertex:
                color = QColor(PALETTE['highlight'])
            elif v in self.visited_vertices:
                color = QColor(PALETTE['sorted'])
            elif v == self.selected_vertex:
                color = QColor(PALETTE['accent_purple'])
            else:
                color = QColor(PALETTE['neutral_bar'])

            painter.setBrush(color)
            painter.setPen(QPen(QColor('#FFFFFF'), 2 if v == self.selected_vertex else 1))
            painter.drawEllipse(int(x - r), int(y - r), r * 2, r * 2)

            painter.setPen(QColor('#FFFFFF' if v not in (self.active_vertex,) else PALETTE['bg_primary']))
            painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
            painter.drawText(int(x - r), int(y - r), r * 2, r * 2, Qt.AlignCenter, v)