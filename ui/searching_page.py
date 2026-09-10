"""
Linear vs Binary Search visualizer with search window tracking.
"""
import random
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QFrame, QMessageBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from algorithms.searching import linear_search, binary_search
from visualization.searching_canvas import SearchingCanvas
from visualization.styles import PALETTE

class SearchingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.array = []
        self.generator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.start_time = 0
        self._init_ui()
        self._generate_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Control Panel
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Linear Search", "Binary Search"])
        self.algo_combo.currentTextChanged.connect(self._on_algo_changed)

        gen_btn = QPushButton("Generate Array")
        gen_btn.clicked.connect(self._generate_data)

        self.sort_btn = QPushButton("Sort Array")
        self.sort_btn.clicked.connect(self._sort_array)

        ctrl_layout.addWidget(QLabel("Algorithm:"))
        ctrl_layout.addWidget(self.algo_combo)
        ctrl_layout.addWidget(gen_btn)
        ctrl_layout.addWidget(self.sort_btn)

        ctrl_layout.addWidget(QLabel("Target Value:"))
        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 999)
        self.target_spin.setValue(42)
        ctrl_layout.addWidget(self.target_spin)

        self.start_btn = QPushButton("Search")
        self.start_btn.setObjectName("action_btn")
        self.start_btn.clicked.connect(self._start)

        self.step_btn = QPushButton("Next Step")
        self.step_btn.clicked.connect(self._step)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self._reset)

        ctrl_layout.addWidget(self.start_btn)
        ctrl_layout.addWidget(self.step_btn)
        ctrl_layout.addWidget(reset_btn)

        layout.addWidget(ctrl_card)

        # Canvas
        self.canvas = SearchingCanvas()
        layout.addWidget(self.canvas)

        # Metrics Card
        self.metrics_card = QFrame()
        self.metrics_card.setObjectName("card")
        metrics_layout = QHBoxLayout(self.metrics_card)
        self.comp_lbl = QLabel("Comparisons: 0")
        self.time_lbl = QLabel("Elapsed: 0.00s")
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_green']};")
        metrics_layout.addWidget(self.comp_lbl)
        metrics_layout.addWidget(self.time_lbl)
        metrics_layout.addWidget(self.status_lbl)
        layout.addWidget(self.metrics_card)

        # Knowledge Panel
        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        self.info_title = QLabel("Complexity Analysis")
        self.info_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.info_desc = QLabel()
        self.info_desc.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        info_layout.addWidget(self.info_title)
        info_layout.addWidget(self.info_desc)
        layout.addWidget(info_card)

        self._on_algo_changed(self.algo_combo.currentText())

    def _generate_data(self):
        self._reset()
        self.array = sorted([random.randint(10, 99) for _ in range(16)])
        if self.array:
            self.target_spin.setValue(self.array[len(self.array) // 2])
        self.canvas.update_state(self.array)

    def _sort_array(self):
        self.array.sort()
        self.canvas.update_state(self.array)
        self.status_lbl.setText("Array sorted.")

    def _on_algo_changed(self, algo):
        if algo == "Binary Search":
            self.info_desc.setText(
                "Binary Search: Best O(1) | Average O(log n) | Worst O(log n) | Space O(1).\n"
                "Requires array to be ordered in monotonic sorted sequence."
            )
        else:
            self.info_desc.setText(
                "Linear Search: Best O(1) | Average O(n) | Worst O(n) | Space O(1).\n"
                "Operates sequentially over arbitrary unordered sequences."
            )

    def _start(self):
        algo = self.algo_combo.currentText()
        if algo == "Binary Search" and self.array != sorted(self.array):
            QMessageBox.warning(self, "Invalid State", "Binary Search requires the array to be sorted first!")
            return

        if self.generator is None:
            target = self.target_spin.value()
            self.generator = binary_search(self.array, target) if algo == "Binary Search" else linear_search(self.array, target)
            self.start_time = time.time()

        self.timer.start(450)
        self.start_btn.setEnabled(False)

    def _step(self):
        algo = self.algo_combo.currentText()
        if algo == "Binary Search" and self.array != sorted(self.array):
            QMessageBox.warning(self, "Invalid State", "Binary Search requires the array to be sorted first!")
            return

        if self.generator is None:
            target = self.target_spin.value()
            self.generator = binary_search(self.array, target) if algo == "Binary Search" else linear_search(self.array, target)
            self.start_time = time.time()

        try:
            state = next(self.generator)
            self.canvas.update_state(self.array, state['index'], state['range'], state['found'])
            self.comp_lbl.setText(f"Comparisons: {state['comparisons']}")
            self.time_lbl.setText(f"Elapsed: {(time.time() - self.start_time):.2f}s")
            self.status_lbl.setText(state['desc'])

            if state['found'] or state['index'] == -1:
                self.timer.stop()
                self.start_btn.setEnabled(False)
        except StopIteration:
            self.timer.stop()

    def _reset(self):
        self.timer.stop()
        self.generator = None
        self.canvas.update_state(self.array)
        self.comp_lbl.setText("Comparisons: 0")
        self.time_lbl.setText("Elapsed: 0.00s")
        self.status_lbl.setText("Ready")
        self.start_btn.setEnabled(True)