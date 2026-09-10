"""
Interactive bar chart canvas for array sorting visualization.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt
from visualization.styles import PALETTE

class SortingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.array = []
        self.highlighted_indices = []
        self.state_type = None
        self.setMinimumHeight(320)

    def update_state(self, array, highlighted_indices=None, state_type=None):
        self.array = list(array)
        self.highlighted_indices = highlighted_indices or []
        self.state_type = state_type
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        painter.fillRect(rect, QColor(PALETTE['bg_card']))

        if not self.array:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.setFont(QFont("Segoe UI", 12))
            painter.drawText(rect, Qt.AlignCenter, "Generate or input data to begin visualization")
            return

        n = len(self.array)
        max_val = max(self.array) if max(self.array) > 0 else 1
        w_avail = rect.width() - 40
        h_avail = rect.height() - 60
        bar_width = max(2.0, (w_avail / n) - 2)
        start_x = 20
        base_y = rect.height() - 30

        # Draw baseline
        painter.setPen(QPen(QColor(PALETTE['border']), 1))
        painter.drawLine(15, base_y, rect.width() - 15, base_y)

        font = QFont("Segoe UI", 8)
        painter.setFont(font)

        for i, val in enumerate(self.array):
            bar_h = (val / max_val) * h_avail
            x = start_x + i * (w_avail / n)
            y = base_y - bar_h

            if self.state_type == 'sorted':
                color = QColor(PALETTE['sorted'])
            elif i in self.highlighted_indices:
                if self.state_type == 'compare':
                    color = QColor(PALETTE['highlight'])
                elif self.state_type in ('swap', 'overwrite'):
                    color = QColor(PALETTE['accent_red'])
                elif self.state_type == 'partition':
                    color = QColor(PALETTE['accent_purple'])
                else:
                    color = QColor(PALETTE['accent_orange'])
            else:
                color = QColor(PALETTE['neutral_bar'])

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(int(x), int(y), int(bar_width), int(bar_h), 2, 2)

            # Draw numeric labels if array is not too dense
            if n <= 30:
                painter.setPen(QColor(PALETTE['text_primary']))
                painter.drawText(int(x), int(base_y + 16), int(bar_width), 14, Qt.AlignCenter, str(val))