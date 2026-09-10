"""
Sorting Visualizer supporting Step-by-Step execution, pause, reset, and live telemetry.
"""
import random
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QFrame
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from algorithms.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort
from visualization.sorting_canvas import SortingCanvas
from visualization.styles import PALETTE

COMPLEXITY_MAP = {
    "Bubble Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)", "stable": "Yes"},
    "Selection Sort": {"best": "O(n²)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)", "stable": "No"},
    "Insertion Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)", "stable": "Yes"},
    "Merge Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "space": "O(n)", "stable": "Yes"},
    "Quick Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n²)", "space": "O(log n)", "stable": "No"}
}

class SortingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initial_array = []
        self.current_array = []
        self.generator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)
        self.start_time = 0
        self.elapsed_time = 0
        self._init_ui()
        self._generate_data("Medium (25)")

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Control Panel
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])
        self.algo_combo.currentTextChanged.connect(self._update_complexity_info)

        self.size_combo = QComboBox()
        self.size_combo.addItems(["Small (12)", "Medium (25)", "Large (50)"])

        gen_btn = QPushButton("Generate Data")
        gen_btn.clicked.connect(lambda: self._generate_data(self.size_combo.currentText()))

        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("action_btn")
        self.start_btn.clicked.connect(self._start)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self._pause)
        self.pause_btn.setEnabled(False)

        self.step_btn = QPushButton("Next Step")
        self.step_btn.clicked.connect(self._step)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self._reset)

        speed_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10, 500)
        self.speed_slider.setValue(100)

        ctrl_layout.addWidget(QLabel("Algorithm:"))
        ctrl_layout.addWidget(self.algo_combo)
        ctrl_layout.addWidget(self.size_combo)
        ctrl_layout.addWidget(gen_btn)
        ctrl_layout.addWidget(self.start_btn)
        ctrl_layout.addWidget(self.pause_btn)
        ctrl_layout.addWidget(self.step_btn)
        ctrl_layout.addWidget(self.reset_btn)
        ctrl_layout.addWidget(speed_label)
        ctrl_layout.addWidget(self.speed_slider)

        layout.addWidget(ctrl_card)

        # Visual Canvas
        self.canvas = SortingCanvas()
        layout.addWidget(self.canvas)

        # Telemetry Bar
        self.telemetry_card = QFrame()
        self.telemetry_card.setObjectName("card")
        telemetry_layout = QHBoxLayout(self.telemetry_card)

        self.comparisons_lbl = QLabel("Comparisons: 0")
        self.swaps_lbl = QLabel("Swaps: 0")
        self.time_lbl = QLabel("Elapsed: 0.00s")
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet(f"color: {PALETTE['accent_green']}; font-weight: bold;")

        telemetry_layout.addWidget(self.comparisons_lbl)
        telemetry_layout.addWidget(self.swaps_lbl)
        telemetry_layout.addWidget(self.time_lbl)
        telemetry_layout.addWidget(self.status_lbl)
        layout.addWidget(self.telemetry_card)

        # Algorithm Complexity & Knowledge Panel
        self.info_card = QFrame()
        self.info_card.setObjectName("card")
        self.info_layout = QVBoxLayout(self.info_card)
        self.info_title = QLabel("Theoretical Complexity")
        self.info_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.info_details = QLabel()
        self.info_details.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        self.info_layout.addWidget(self.info_title)
        self.info_layout.addWidget(self.info_details)
        layout.addWidget(self.info_card)

        self._update_complexity_info(self.algo_combo.currentText())

    def _generate_data(self, size_str):
        self._reset()
        count = 25
        if "12" in size_str:
            count = 12
        elif "50" in size_str:
            count = 50
        self.initial_array = [random.randint(5, 100) for _ in range(count)]
        self.current_array = list(self.initial_array)
        self.canvas.update_state(self.current_array)
        self.status_lbl.setText("Data loaded")

    def _get_selected_algorithm(self):
        algo = self.algo_combo.currentText()
        if algo == "Bubble Sort":
            return bubble_sort(self.current_array)
        elif algo == "Selection Sort":
            return selection_sort(self.current_array)
        elif algo == "Insertion Sort":
            return insertion_sort(self.current_array)
        elif algo == "Merge Sort":
            return merge_sort(self.current_array)
        elif algo == "Quick Sort":
            return quick_sort(self.current_array)

    def _start(self):
        if self.generator is None:
            self.generator = self._get_selected_algorithm()
            self.start_time = time.time() - self.elapsed_time

        interval = 520 - self.speed_slider.value()
        self.timer.start(interval)
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.status_lbl.setText("Sorting in progress...")

    def _pause(self):
        self.timer.stop()
        self.elapsed_time = time.time() - self.start_time
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.status_lbl.setText("Paused")

    def _step(self):
        if self.generator is None:
            self.generator = self._get_selected_algorithm()
            self.start_time = time.time()

        try:
            op = next(self.generator)
            self.current_array = op['array']
            self.canvas.update_state(self.current_array, op['indices'], op['type'])
            self.comparisons_lbl.setText(f"Comparisons: {op['comparisons']}")
            self.swaps_lbl.setText(f"Swaps: {op['swaps']}")
            self.elapsed_time = time.time() - self.start_time
            self.time_lbl.setText(f"Elapsed: {self.elapsed_time:.2f}s")
            self.status_lbl.setText(op['desc'])

            if op['type'] == 'sorted':
                self.timer.stop()
                self.start_btn.setEnabled(False)
                self.pause_btn.setEnabled(False)
                self.status_lbl.setText("Sorting completed.")
        except StopIteration:
            self.timer.stop()
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.status_lbl.setText("Sorting completed.")

    def _reset(self):
        self.timer.stop()
        self.generator = None
        self.current_array = list(self.initial_array)
        self.canvas.update_state(self.current_array)
        self.comparisons_lbl.setText("Comparisons: 0")
        self.swaps_lbl.setText("Swaps: 0")
        self.time_lbl.setText("Elapsed: 0.00s")
        self.elapsed_time = 0
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.status_lbl.setText("Reset to initial state")

    def _update_complexity_info(self, algo_name):
        info = COMPLEXITY_MAP.get(algo_name, {})
        self.info_details.setText(
            f"Algorithm: {algo_name} | Best: {info.get('best')} | "
            f"Average: {info.get('avg')} | Worst: {info.get('worst')} | "
            f"Space Complexity: {info.get('space')} | Stable: {info.get('stable')}"
        )