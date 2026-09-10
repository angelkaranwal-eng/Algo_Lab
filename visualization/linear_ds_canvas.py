"""
Renders Node-based Stack, Queue, Circular Queue, and Linked List structures.
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QPolygon
from PySide6.QtCore import Qt, QPoint
from visualization.styles import PALETTE

class LinearDSCanvas(QWidget):
    def __init__(self, mode="stack", parent=None):
        super().__init__(parent)
        self.mode = mode  # "stack", "queue", "circular_queue", "linked_list"
        self.elements = []
        self.metadata = {}
        self.setMinimumHeight(280)

    def set_data(self, elements, metadata=None):
        self.elements = list(elements)
        self.metadata = metadata or {}
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor(PALETTE['bg_card']))

        if self.mode == "stack":
            self._draw_stack(painter, rect)
        elif self.mode == "queue":
            self._draw_queue(painter, rect)
        elif self.mode == "circular_queue":
            self._draw_circular_queue(painter, rect)
        elif self.mode == "linked_list":
            self._draw_linked_list(painter, rect)

    def _draw_stack(self, painter, rect):
        if not self.elements:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(rect, Qt.AlignCenter, "Stack is empty (Underflow)")
            return

        w, h = 140, 36
        cx = rect.width() / 2 - (w / 2)
        base_y = rect.height() - 40

        for i, val in enumerate(self.elements):
            y = base_y - (i + 1) * (h + 6)
            is_top = (i == len(self.elements) - 1)
            painter.setBrush(QColor(PALETTE['accent_blue'] if is_top else PALETTE['bg_card_secondary']))
            painter.setPen(QPen(QColor(PALETTE['border']), 1))
            painter.drawRoundedRect(int(cx), int(y), w, h, 6, 6)

            painter.setPen(QColor('#FFFFFF' if is_top else PALETTE['text_primary']))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(int(cx), int(y), w, h, Qt.AlignCenter, str(val))

            if is_top:
                painter.setPen(QColor(PALETTE['accent_orange']))
                painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
                painter.drawText(int(cx + w + 10), int(y + 22), "← TOP")

    def _draw_queue(self, painter, rect):
        if not self.elements:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(rect, Qt.AlignCenter, "Queue is empty")
            return

        w, h = 60, 50
        cy = (rect.height() - h) / 2
        n = len(self.elements)
        start_x = (rect.width() - (n * (w + 12))) / 2

        for i, val in enumerate(self.elements):
            x = start_x + i * (w + 12)
            is_front = (i == 0)
            is_rear = (i == n - 1)

            color = PALETTE['accent_green'] if is_front else (PALETTE['accent_blue'] if is_rear else PALETTE['bg_card_secondary'])
            painter.setBrush(QColor(color))
            painter.setPen(QPen(QColor(PALETTE['border']), 1))
            painter.drawRoundedRect(int(x), int(cy), w, h, 6, 6)

            painter.setPen(QColor('#FFFFFF'))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(int(x), int(cy), w, h, Qt.AlignCenter, str(val))

            painter.setFont(QFont("Segoe UI", 8, QFont.Bold))
            if is_front:
                painter.setPen(QColor(PALETTE['accent_green']))
                painter.drawText(int(x), int(cy - 8), w, 14, Qt.AlignCenter, "FRONT")
            if is_rear:
                painter.setPen(QColor(PALETTE['accent_blue']))
                painter.drawText(int(x), int(cy + h + 16), w, 14, Qt.AlignCenter, "REAR")

    def _draw_circular_queue(self, painter, rect):
        buffer = self.metadata.get('buffer', [])
        front = self.metadata.get('front', -1)
        rear = self.metadata.get('rear', -1)

        n = len(buffer)
        if n == 0:
            return

        w, h = 54, 50
        start_x = (rect.width() - (n * (w + 8))) / 2
        cy = (rect.height() - h) / 2

        for i in range(n):
            x = start_x + i * (w + 8)
            val = buffer[i]

            is_active = (val is not None)
            painter.setBrush(QColor(PALETTE['bg_card_secondary'] if is_active else PALETTE['bg_primary']))
            border = PALETTE['accent_blue'] if (i == front or i == rear) else PALETTE['border']
            painter.setPen(QPen(QColor(border), 2 if (i == front or i == rear) else 1))
            painter.drawRoundedRect(int(x), int(cy), w, h, 6, 6)

            val_str = str(val) if val is not None else "-"
            painter.setPen(QColor(PALETTE['text_primary'] if is_active else PALETTE['text_secondary']))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(int(x), int(cy), w, h, Qt.AlignCenter, val_str)

            # Slot index
            painter.setFont(QFont("Segoe UI", 8))
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(int(x), int(cy + h + 14), w, 14, Qt.AlignCenter, f"idx:{i}")

            markers = []
            if i == front:
                markers.append("F")
            if i == rear:
                markers.append("R")
            if markers:
                painter.setPen(QColor(PALETTE['highlight']))
                painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
                painter.drawText(int(x), int(cy - 8), w, 14, Qt.AlignCenter, "/".join(markers))

    def _draw_linked_list(self, painter, rect):
        if not self.elements:
            painter.setPen(QColor(PALETTE['text_secondary']))
            painter.drawText(rect, Qt.AlignCenter, "Linked List is empty (Head is NULL)")
            return

        node_w, node_h = 75, 42
        gap = 35
        n = len(self.elements)
        start_x = 30
        cy = (rect.height() - node_h) / 2

        active_idx = self.metadata.get('active_idx', -1)

        for i, val in enumerate(self.elements):
            x = start_x + i * (node_w + gap)

            # Draw Node Body [ Data | Ptr ]
            is_active = (i == active_idx)
            painter.setBrush(QColor(PALETTE['highlight'] if is_active else PALETTE['bg_card_secondary']))
            painter.setPen(QPen(QColor(PALETTE['border']), 1))
            painter.drawRoundedRect(int(x), int(cy), node_w, node_h, 6, 6)

            # Divider line inside node
            div_x = x + node_w - 24
            painter.drawLine(int(div_x), int(cy), int(div_x), int(cy + node_h))

            # Value
            painter.setPen(QColor(PALETTE['bg_primary'] if is_active else PALETTE['text_primary']))
            painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
            painter.drawText(int(x), int(cy), node_w - 24, node_h, Qt.AlignCenter, str(val))

            # Pointer dot
            painter.setBrush(QColor(PALETTE['accent_blue']))
            painter.drawEllipse(int(div_x + 8), int(cy + node_h / 2 - 4), 8, 8)

            # Arrow to next node or NULL
            arrow_start_x = x + node_w
            arrow_end_x = arrow_start_x + gap
            arrow_y = cy + node_h / 2

            painter.setPen(QPen(QColor(PALETTE['accent_blue']), 2))
            painter.drawLine(int(arrow_start_x), int(arrow_y), int(arrow_end_x), int(arrow_y))

            # Draw arrowhead
            poly = QPolygon([
                QPoint(int(arrow_end_x), int(arrow_y)),
                QPoint(int(arrow_end_x - 6), int(arrow_y - 4)),
                QPoint(int(arrow_end_x - 6), int(arrow_y + 4))
            ])
            painter.setBrush(QColor(PALETTE['accent_blue']))
            painter.drawPolygon(poly)

            if i == 0:
                painter.setPen(QColor(PALETTE['accent_green']))
                painter.setFont(QFont("Segoe UI", 8, QFont.Bold))
                painter.drawText(int(x), int(cy - 8), node_w, 14, Qt.AlignCenter, "HEAD")

        # Terminal NULL marker
        last_x = start_x + n * (node_w + gap)
        painter.setPen(QColor(PALETTE['text_secondary']))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(int(last_x), int(cy), 50, node_h, Qt.AlignVCenter | Qt.AlignLeft, "NULL")