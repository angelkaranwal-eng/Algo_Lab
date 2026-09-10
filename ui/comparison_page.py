"""
Side-by-side empirical benchmarking module executing actual sorting passes on identical datasets.
"""
import random
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QFont
from algorithms.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort
from visualization.styles import PALETTE

class ComparisonPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Algorithm Performance Analysis & Benchmark")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        subtitle = QLabel("Runs algorithms on identical input datasets. Telemetry is collected from actual program execution.")
        subtitle.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QHBoxLayout(ctrl_card)

        self.size_combo = QComboBox()
        self.size_combo.addItems(["50 Elements", "150 Elements", "300 Elements"])

        run_btn = QPushButton("Execute Benchmark Suite")
        run_btn.setObjectName("action_btn")
        run_btn.clicked.connect(self._run_benchmark)

        ctrl_layout.addWidget(QLabel("Dataset Size:"))
        ctrl_layout.addWidget(self.size_combo)
        ctrl_layout.addWidget(run_btn)
        ctrl_layout.addStretch()
        layout.addWidget(ctrl_card)

        # Benchmark Results Table
        self.table = QTableWidget(5, 6)
        self.table.setHorizontalHeaderLabels([
            "Algorithm", "Time (ms)", "Comparisons", "Swaps / Overwrites", "Theoretical Time", "Space Complexity"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Educational Note
        note_card = QFrame()
        note_card.setObjectName("card")
        note_layout = QVBoxLayout(note_card)
        t_note = QLabel("Understanding Experimental Measurements")
        t_note.setFont(QFont("Segoe UI", 11, QFont.Bold))
        d_note = QLabel(
            "• Wall-clock execution time depends on CPU architectures, memory cache hierarchies, and interpreter overhead.\n"
            "• Asymptotic big-O analysis bounds asymptotic growth, while comparison count demonstrates operational work independent of CPU clock speeds."
        )
        d_note.setStyleSheet(f"color: {PALETTE['text_secondary']};")
        note_layout.addWidget(t_note)
        note_layout.addWidget(d_note)
        layout.addWidget(note_card)

    def _run_benchmark(self):
        size_str = self.size_combo.currentText()
        count = int(size_str.split()[0])
        dataset = [random.randint(1, 1000) for _ in range(count)]

        algorithms = [
            ("Bubble Sort", bubble_sort, "O(n²)", "O(1)"),
            ("Selection Sort", selection_sort, "O(n²)", "O(1)"),
            ("Insertion Sort", insertion_sort, "O(n²)", "O(1)"),
            ("Merge Sort", merge_sort, "O(n log n)", "O(n)"),
            ("Quick Sort", quick_sort, "O(n log n)", "O(log n)"),
        ]

        for row, (name, fn, t_time, s_space) in enumerate(algorithms):
            data_copy = list(dataset)
            t_start = time.perf_counter()
            gen = fn(data_copy)
            final_event = None
            for event in gen:
                final_event = event
            elapsed_ms = (time.perf_counter() - t_start) * 1000

            comps = final_event.get('comparisons', 0) if final_event else 0
            swaps = final_event.get('swaps', 0) if final_event else 0

            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{elapsed_ms:.2f} ms"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{comps:,}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{swaps:,}"))
            self.table.setItem(row, 4, QTableWidgetItem(t_time))
            self.table.setItem(row, 5, QTableWidgetItem(s_space))