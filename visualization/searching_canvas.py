"""
Searching Canvas displaying arrays as distinct indexed block cells.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt
from visualization.styles import PALETTE

class SearchingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.array = []
        self.active_idx = -1
        self.search_range = None
        self.found = False
        self.setMinimumHeight(240)

    def update_state(self, array, active_idx=-1, search_range=None, found=False):
        self.array = list(array)
        self.active_idx = active_idx
        self.search_range = search_range
        self.found = found
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor(PALETTE['bg_card']))

        if not self.array:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.setFont(QFont("Segoe UI", 12))
            painter.drawText(rect, Qt.AlignCenter, "Generate data and specify a target to search")
            return

        n = len(self.array)
        box_w = min(50.0, (rect.width() - 40) / n)
        box_h = 50.0
        start_x = (rect.width() - (n * box_w)) / 2
        y = (rect.height() - box_h) / 2

        low, high = (self.search_range if self.search_range else (0, n - 1))

        for i, val in enumerate(self.array):
            x = start_x + i * box_w
            # Determine cell visual state
            if i == self.active_idx:
                color = QColor(PALETTE['sorted'] if self.found else PALETTE['highlight'])
                border_color = QColor('#FFFFFF')
            elif low <= i <= high:
                color = QColor(PALETTE['bg_card_secondary'])
                border_color = QColor(PALETTE['accent_blue'])
            else:
                color = QColor(PALETTE['bg_primary'])  # Out of search scope
                border_color = QColor(PALETTE['border'])

            painter.setBrush(color)
            painter.setPen(QPen(border_color, 2 if i == self.active_idx else 1))
            painter.drawRoundedRect(int(x + 2), int(y), int(box_w - 4), int(box_h), 4, 4)

            # Draw value
            painter.setPen(QColor(PALETTE['text_primary'] if low <= i <= high else PALETTE['text_secondary']))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(int(x), int(y), int(box_w), int(box_h), Qt.AlignCenter, str(val))

            # Draw index
            painter.setFont(QFont("Segoe UI", 8))
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(int(x), int(y + box_h + 8), int(box_w), 16, Qt.AlignCenter, f"[{i}]")