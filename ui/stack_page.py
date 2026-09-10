"""
Stack Visualizer (LIFO Principle) backed by NodeBasedStack.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFrame, QMessageBox
)
from PySide6.QtGui import QFont
from data_structures.stack import NodeBasedStack
from visualization.linear_ds_canvas import LinearDSCanvas
from visualization.styles import PALETTE

class StackPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stack = NodeBasedStack(max_capacity=7)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Control Strip
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.val_spin = QSpinBox()
        self.val_spin.setRange(1, 999)
        self.val_spin.setValue(10)

        push_btn = QPushButton("Push Value")
        push_btn.setObjectName("action_btn")
        push_btn.clicked.connect(self._push)

        pop_btn = QPushButton("Pop Value")
        pop_btn.clicked.connect(self._pop)

        peek_btn = QPushButton("Peek")
        peek_btn.clicked.connect(self._peek)

        clear_btn = QPushButton("Clear Stack")
        clear_btn.clicked.connect(self._clear)

        ctrl_layout.addWidget(QLabel("Node Value:"))
        ctrl_layout.addWidget(self.val_spin)
        ctrl_layout.addWidget(push_btn)
        ctrl_layout.addWidget(pop_btn)
        ctrl_layout.addWidget(peek_btn)
        ctrl_layout.addWidget(clear_btn)
        layout.addWidget(ctrl_card)

        # Visual Canvas
        self.canvas = LinearDSCanvas(mode="stack")
        layout.addWidget(self.canvas)

        # Telemetry Card
        self.telemetry = QFrame()
        self.telemetry.setObjectName("card")
        t_layout = QHBoxLayout(self.telemetry)
        self.size_lbl = QLabel("Size: 0 / 7")
        self.ops_lbl = QLabel("Push Count: 0 | Pop Count: 0")
        self.status_lbl = QLabel("Principle: Last In, First Out (LIFO)")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_blue']}; font-weight: bold;")
        t_layout.addWidget(self.size_lbl)
        t_layout.addWidget(self.ops_lbl)
        t_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry)

        # Complexity Card
        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        t_info = QLabel("Stack Operations & Complexity")
        t_info.setFont(QFont("Segoe UI", 11, QFont.Bold))
        d_info = QLabel("Push: O(1) | Pop: O(1) | Peek: O(1) | Space: O(n)\nManual custom implementation uses linked nodes without contiguous array resizing.")
        d_info.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        info_layout.addWidget(t_info)
        info_layout.addWidget(d_info)
        layout.addWidget(info_card)

    def _push(self):
        val = self.val_spin.value()
        if not self.stack.push(val):
            QMessageBox.critical(self, "Stack Overflow", "Cannot push: Stack has reached its maximum capacity of 7 elements!")
            return
        # Display elements bottom-to-top
        self.canvas.set_data(reversed(self.stack.to_list()))
        self._update_telemetry(f"Pushed node with value {val} to top.")

    def _pop(self):
        if self.stack.is_empty():
            QMessageBox.warning(self, "Stack Underflow", "Cannot pop from an empty stack!")
            return
        removed = self.stack.pop()
        self.canvas.set_data(reversed(self.stack.to_list()))
        self._update_telemetry(f"Popped node {removed} from stack.")

    def _peek(self):
        val = self.stack.peek()
        if val is None:
            QMessageBox.information(self, "Peek Result", "Stack is empty.")
        else:
            QMessageBox.information(self, "Peek Result", f"Current Top Element: {val}")

    def _clear(self):
        self.stack.clear()
        self.canvas.set_data([])
        self._update_telemetry("Stack reset.")

    def _update_telemetry(self, status):
        self.size_lbl.setText(f"Size: {self.stack.size()} / {self.stack.max_capacity}")
        self.ops_lbl.setText(f"Push Count: {self.stack.push_count} | Pop Count: {self.stack.pop_count}")
        self.status_lbl.setText(status)