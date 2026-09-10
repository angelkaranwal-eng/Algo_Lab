"""
Binary Search Tree Visualizer: dynamic node comparisons, balanced visual layouts, and traversals.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFrame, QMessageBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from data_structures.binary_search_tree import BinarySearchTree
from visualization.bst_canvas import BSTCanvas
from visualization.styles import PALETTE

class TreePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bst = BinarySearchTree()
        self.anim_gen = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step_animation)
        self._init_ui()

        # Seed standard educational tree
        for k in [50, 30, 70, 20, 40, 60, 80]:
            list(self.bst.insert(k))
        self._refresh()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.key_spin = QSpinBox()
        self.key_spin.setRange(1, 999)
        self.key_spin.setValue(65)

        ins_btn = QPushButton("Insert Key")
        ins_btn.setObjectName("action_btn")
        ins_btn.clicked.connect(self._insert)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._search)

        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self._delete)

        inorder_btn = QPushButton("Inorder Traversal")
        inorder_btn.clicked.connect(self._inorder)

        preorder_btn = QPushButton("Preorder")
        preorder_btn.clicked.connect(self._preorder)

        postorder_btn = QPushButton("Postorder")
        postorder_btn.clicked.connect(self._postorder)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear)

        ctrl_layout.addWidget(QLabel("Key:"))
        ctrl_layout.addWidget(self.key_spin)
        ctrl_layout.addWidget(ins_btn)
        ctrl_layout.addWidget(search_btn)
        ctrl_layout.addWidget(del_btn)
        ctrl_layout.addWidget(inorder_btn)
        ctrl_layout.addWidget(preorder_btn)
        ctrl_layout.addWidget(postorder_btn)
        ctrl_layout.addWidget(clear_btn)
        layout.addWidget(ctrl_card)

        # Canvas
        self.canvas = BSTCanvas()
        layout.addWidget(self.canvas)

        # Metrics Card
        self.telemetry = QFrame()
        self.telemetry.setObjectName("card")
        t_layout = QHBoxLayout(self.telemetry)
        self.size_lbl = QLabel("Nodes: 0")
        self.height_lbl = QLabel("Height: 0")
        self.status_lbl = QLabel("BST Initialized")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_green']};")
        t_layout.addWidget(self.size_lbl)
        t_layout.addWidget(self.height_lbl)
        t_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry)

        # Info Card
        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        t_info = QLabel("BST Properties & Algorithmic Guarantees")
        t_info.setFont(QFont("Segoe UI", 11, QFont.Bold))
        d_info = QLabel(
            "Average Time: Search O(log n), Insert O(log n), Delete O(log n) | Worst Case (skewed): O(n)\n"
            "Key Principle: Inorder traversal of a BST visits Left-Root-Right, yielding values in monotonic sorted order."
        )
        d_info.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        info_layout.addWidget(t_info)
        info_layout.addWidget(d_info)
        layout.addWidget(info_card)

    def _insert(self):
        k = self.key_spin.value()
        self.anim_gen = self.bst.insert(k)
        self.timer.start(350)

    def _search(self):
        k = self.key_spin.value()
        self.anim_gen = self.bst.search(k)
        self.timer.start(350)

    def _delete(self):
        k = self.key_spin.value()
        if not self.bst.delete(k):
            QMessageBox.warning(self, "Not Found", f"Key {k} does not exist in BST.")
        else:
            self._refresh(f"Deleted key {k}.")

    def _inorder(self):
        keys = self.bst.inorder()
        self.status_lbl.setText(f"Inorder Traversal (Sorted): {' → '.join(map(str, keys))}")

    def _preorder(self):
        keys = self.bst.preorder()
        self.status_lbl.setText(f"Preorder (Root-Left-Right): {' → '.join(map(str, keys))}")

    def _postorder(self):
        keys = self.bst.postorder()
        self.status_lbl.setText(f"Postorder (Left-Right-Root): {' → '.join(map(str, keys))}")

    def _clear(self):
        self.bst.clear()
        self._refresh("BST cleared.")

    def _step_animation(self):
        try:
            step = next(self.anim_gen)
            action = step[0]
            if action == 'compare':
                curr, target, branch = step[1], step[2], step[3]
                self.canvas.set_tree(self.bst, highlight_key=curr)
                self.status_lbl.setText(f"Comparing target {target} with node {curr} -> Traversing {branch}")
            elif action == 'placed':
                k = step[1]
                self.canvas.set_tree(self.bst, highlight_key=k)
                self.status_lbl.setText(f"Inserted new key {k} into tree structure.")
                self.timer.stop()
                self._refresh()
            elif action == 'visit':
                curr, found = step[1], step[2]
                self.canvas.set_tree(self.bst, highlight_key=curr)
                if found:
                    self.status_lbl.setText(f"Found search target {curr}!")
                    self.timer.stop()
                else:
                    self.status_lbl.setText(f"Inspecting key {curr}...")
            elif action == 'duplicate':
                self.status_lbl.setText(f"Duplicate key {step[1]} rejected.")
                self.timer.stop()
            elif action == 'not_found':
                self.status_lbl.setText(f"Target key {step[1]} does not exist in tree.")
                self.timer.stop()
        except StopIteration:
            self.timer.stop()
            self._refresh()

    def _refresh(self, status_msg=None):
        self.canvas.set_tree(self.bst)
        self.size_lbl.setText(f"Nodes: {self.bst.size()}")
        self.height_lbl.setText(f"Height: {self.bst.height()}")
        if status_msg:
            self.status_lbl.setText(status_msg)