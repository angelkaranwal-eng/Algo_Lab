"""
Queue Visualizer (FIFO) supporting both Node-based Queue and Circular Queue implementations.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox, QFrame, QMessageBox
)
from PySide6.QtGui import QFont
from data_structures.queue import NodeBasedQueue
from data_structures.circular_queue import CircularQueue
from visualization.linear_ds_canvas import LinearDSCanvas
from visualization.styles import PALETTE

class QueuePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.node_queue = NodeBasedQueue(max_capacity=8)
        self.circ_queue = CircularQueue(capacity=8)
        self.is_circular = False
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Simple Node Queue (FIFO)", "Circular Array Queue"])
        self.mode_combo.currentTextChanged.connect(self._toggle_mode)

        self.val_spin = QSpinBox()
        self.val_spin.setRange(1, 999)
        self.val_spin.setValue(20)

        enq_btn = QPushButton("Enqueue")
        enq_btn.setObjectName("action_btn")
        enq_btn.clicked.connect(self._enqueue)

        deq_btn = QPushButton("Dequeue")
        deq_btn.clicked.connect(self._dequeue)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear)

        ctrl_layout.addWidget(QLabel("Queue Model:"))
        ctrl_layout.addWidget(self.mode_combo)
        ctrl_layout.addWidget(QLabel("Value:"))
        ctrl_layout.addWidget(self.val_spin)
        ctrl_layout.addWidget(enq_btn)
        ctrl_layout.addWidget(deq_btn)
        ctrl_layout.addWidget(clear_btn)
        layout.addWidget(ctrl_card)

        # Canvas
        self.canvas = LinearDSCanvas(mode="queue")
        layout.addWidget(self.canvas)

        # Telemetry
        self.telemetry = QFrame()
        self.telemetry.setObjectName("card")
        t_layout = QHBoxLayout(self.telemetry)
        self.size_lbl = QLabel("Size: 0 / 8")
        self.ptrs_lbl = QLabel("Front: None | Rear: None")
        self.status_lbl = QLabel("Principle: First In, First Out (FIFO)")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_green']}; font-weight: bold;")
        t_layout.addWidget(self.size_lbl)
        t_layout.addWidget(self.ptrs_lbl)
        t_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry)

        # Theory card
        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        t_info = QLabel("Queue Mechanics & Time Complexity")
        t_info.setFont(QFont("Segoe UI", 11, QFont.Bold))
        d_info = QLabel("Enqueue: O(1) | Dequeue: O(1) | Front/Rear: O(1) | Space: O(n)\nCircular queues reuse memory by wrapping pointers: (rear + 1) % capacity.")
        d_info.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        info_layout.addWidget(t_info)
        info_layout.addWidget(d_info)
        layout.addWidget(info_card)

    def _toggle_mode(self, mode_str):
        self.is_circular = ("Circular" in mode_str)
        self.canvas.mode = "circular_queue" if self.is_circular else "queue"
        self._sync_canvas("Switched queue model.")

    def _enqueue(self):
        val = self.val_spin.value()
        if self.is_circular:
            if not self.circ_queue.enqueue(val):
                QMessageBox.critical(self, "Queue Overflow", "Circular Queue is completely full!")
                return
        else:
            if not self.node_queue.enqueue(val):
                QMessageBox.critical(self, "Queue Overflow", "Node Queue reached its maximum limit!")
                return
        self._sync_canvas(f"Enqueued element {val} at rear.")

    def _dequeue(self):
        if self.is_circular:
            if self.circ_queue.is_empty():
                QMessageBox.warning(self, "Queue Underflow", "Queue is empty!")
                return
            removed = self.circ_queue.dequeue()
        else:
            if self.node_queue.is_empty():
                QMessageBox.warning(self, "Queue Underflow", "Queue is empty!")
                return
            removed = self.node_queue.dequeue()
        self._sync_canvas(f"Dequeued element {removed} from front.")

    def _clear(self):
        self.circ_queue.clear()
        self.node_queue.clear()
        self._sync_canvas("Queue cleared.")

    def _sync_canvas(self, status_msg):
        if self.is_circular:
            meta = {
                'buffer': self.circ_queue.buffer,
                'front': self.circ_queue.front_idx,
                'rear': self.circ_queue.rear_idx
            }
            self.canvas.set_data(self.circ_queue.buffer, metadata=meta)
            self.size_lbl.setText(f"Size: {self.circ_queue.size()} / {self.circ_queue.capacity}")
            self.ptrs_lbl.setText(f"Front Idx: {self.circ_queue.front_idx} | Rear Idx: {self.circ_queue.rear_idx}")
        else:
            data = self.node_queue.to_list()
            self.canvas.set_data(data)
            self.size_lbl.setText(f"Size: {self.node_queue.size()} / {self.node_queue.max_capacity}")
            self.ptrs_lbl.setText(f"Front: {self.node_queue.front()} | Rear: {self.node_queue.rear()}")

        self.status_lbl.setText(status_msg)