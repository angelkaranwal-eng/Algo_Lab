"""
Singly Linked List Visualizer: head, node insertions, deletions, pointer reversals, and linear walk.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFrame, QMessageBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from data_structures.linked_list import SinglyLinkedList
from visualization.linear_ds_canvas import LinearDSCanvas
from visualization.styles import PALETTE

class LinkedListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ll = SinglyLinkedList()
        self.search_gen = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step_search)
        self._init_ui()

        for val in [10, 20, 30, 40]:
            self.ll.insert_at_end(val)
        self._refresh()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Operations
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.val_spin = QSpinBox()
        self.val_spin.setRange(1, 999)
        self.val_spin.setValue(50)

        self.pos_spin = QSpinBox()
        self.pos_spin.setRange(0, 20)
        self.pos_spin.setValue(0)

        ins_beg_btn = QPushButton("Insert Head")
        ins_beg_btn.clicked.connect(self._insert_head)

        ins_end_btn = QPushButton("Insert Tail")
        ins_end_btn.clicked.connect(self._insert_tail)

        ins_pos_btn = QPushButton("Insert @ Pos")
        ins_pos_btn.clicked.connect(self._insert_pos)

        del_beg_btn = QPushButton("Delete Head")
        del_beg_btn.clicked.connect(self._delete_head)

        del_end_btn = QPushButton("Delete Tail")
        del_end_btn.clicked.connect(self._delete_tail)

        rev_btn = QPushButton("Reverse Pointers")
        rev_btn.setObjectName("action_btn")
        rev_btn.clicked.connect(self._reverse)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._search)

        ctrl_layout.addWidget(QLabel("Val:"))
        ctrl_layout.addWidget(self.val_spin)
        ctrl_layout.addWidget(QLabel("Pos:"))
        ctrl_layout.addWidget(self.pos_spin)
        ctrl_layout.addWidget(ins_beg_btn)
        ctrl_layout.addWidget(ins_end_btn)
        ctrl_layout.addWidget(ins_pos_btn)
        ctrl_layout.addWidget(del_beg_btn)
        ctrl_layout.addWidget(del_end_btn)
        ctrl_layout.addWidget(rev_btn)
        ctrl_layout.addWidget(search_btn)
        layout.addWidget(ctrl_card)

        # Canvas
        self.canvas = LinearDSCanvas(mode="linked_list")
        layout.addWidget(self.canvas)

        # Telemetry
        self.telemetry = QFrame()
        self.telemetry.setObjectName("card")
        t_layout = QHBoxLayout(self.telemetry)
        self.nodes_lbl = QLabel("Node Count: 0")
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_green']};")
        t_layout.addWidget(self.nodes_lbl)
        t_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry)

        # Complexity
        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        t_info = QLabel("Complexity Analysis")
        t_info.setFont(QFont("Segoe UI", 11, QFont.Bold))
        d_info = QLabel(
            "Insert at Head: O(1) | Insert at Tail: O(n) | Insert at Position: O(n)\n"
            "Delete Head: O(1) | Delete Tail: O(n) | Search: O(n) | Reverse: O(n) time & O(1) auxiliary space"
        )
        d_info.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        info_layout.addWidget(t_info)
        info_layout.addWidget(d_info)
        layout.addWidget(info_card)

    def _insert_head(self):
        val = self.val_spin.value()
        self.ll.insert_at_beginning(val)
        self._refresh(f"Inserted {val} at head.")

    def _insert_tail(self):
        val = self.val_spin.value()
        self.ll.insert_at_end(val)
        self._refresh(f"Inserted {val} at tail.")

    def _insert_pos(self):
        val = self.val_spin.value()
        pos = self.pos_spin.value()
        if not self.ll.insert_at_position(val, pos):
            QMessageBox.warning(self, "Invalid Position", f"Cannot insert at index {pos}. Bounds: [0, {self.ll.size()}]")
            return
        self._refresh(f"Inserted {val} at index {pos}.")

    def _delete_head(self):
        if self.ll.is_empty():
            QMessageBox.warning(self, "List Empty", "Underflow: List is empty.")
            return
        val = self.ll.delete_from_beginning()
        self._refresh(f"Deleted head node ({val}).")

    def _delete_tail(self):
        if self.ll.is_empty():
            QMessageBox.warning(self, "List Empty", "Underflow: List is empty.")
            return
        val = self.ll.delete_from_end()
        self._refresh(f"Deleted tail node ({val}).")

    def _reverse(self):
        self.ll.reverse()
        self._refresh("Pointers reversed in-place.")

    def _search(self):
        target = self.val_spin.value()
        self.search_gen = self.ll.search_steps(target)
        self.timer.start(400)

    def _step_search(self):
        try:
            idx, val, found = next(self.search_gen)
            if idx == -1:
                self.timer.stop()
                self.canvas.set_data(self.ll.to_list(), metadata={'active_idx': -1})
                self.status_lbl.setText("Target not found in linked list.")
            else:
                self.canvas.set_data(self.ll.to_list(), metadata={'active_idx': idx})
                if found:
                    self.timer.stop()
                    self.status_lbl.setText(f"Target found at node index {idx}!")
                else:
                    self.status_lbl.setText(f"Comparing with node [{idx}] = {val}...")
        except StopIteration:
            self.timer.stop()

    def _refresh(self, status_msg="Ready"):
        self.canvas.set_data(self.ll.to_list(), metadata={'active_idx': -1})
        self.nodes_lbl.setText(f"Node Count: {self.ll.size()}")
        self.status_lbl.setText(status_msg)