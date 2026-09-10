"""
Dynamic tree visualizer for Binary Search Trees with coordinate recursion.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt
from visualization.styles import PALETTE

class BSTCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bst = None
        self.highlight_key = None
        self.setMinimumHeight(340)

    def set_tree(self, bst, highlight_key=None):
        self.bst = bst
        self.highlight_key = highlight_key
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor(PALETTE['bg_card']))

        if not self.bst or self.bst.root is None:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(rect, Qt.AlignCenter, "Binary Search Tree is empty. Insert keys to construct tree.")
            return

        self._draw_node(painter, self.bst.root, rect.width() / 2, 40, rect.width() / 4)

    def _draw_node(self, painter, node, x, y, offset):
        if node is None:
            return

        radius = 20

        # Draw connecting edges to children first
        painter.setPen(QPen(QColor(PALETTE['border']), 2))
        child_y = y + 60
        if node.left:
            child_x = x - offset
            painter.drawLine(int(x), int(y), int(child_x), int(child_y))
            self._draw_node(painter, node.left, child_x, child_y, max(offset / 2, 24))

        if node.right:
            child_x = x + offset
            painter.drawLine(int(x), int(y), int(child_x), int(child_y))
            self._draw_node(painter, node.right, child_x, child_y, max(offset / 2, 24))

        # Draw Node
        is_highlighted = (node.key == self.highlight_key)
        painter.setBrush(QColor(PALETTE['highlight'] if is_highlighted else PALETTE['neutral_bar']))
        painter.setPen(QPen(QColor('#FFFFFF' if is_highlighted else PALETTE['border']), 2))
        painter.drawEllipse(int(x - radius), int(y - radius), int(radius * 2), int(radius * 2))

        # Draw Node Key
        painter.setPen(QColor(PALETTE['bg_primary'] if is_highlighted else '#FFFFFF'))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(int(x - radius), int(y - radius), int(radius * 2), int(radius * 2), Qt.AlignCenter, str(node.key))