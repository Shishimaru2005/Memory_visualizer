from memory_algorithms import calculate_fragmentation, first_fit, best_fit, worst_fit
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRectF
from utils import generate_memory_blocks

class Visualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Management Visualizer")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.memory_blocks = generate_memory_blocks(400, [100, 50, 75, 125, 50])
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.input_size = QLineEdit()
        self.input_size.setPlaceholderText("Process size")
        self.layout.addWidget(self.input_size)

        self.algorithms = {
            "First Fit": first_fit,
            "Best Fit": best_fit,
            "Worst Fit": worst_fit
        }

        self.dropdown = QComboBox()
        self.dropdown.addItems(self.algorithms.keys())
        self.layout.addWidget(self.dropdown)

        self.add_button = QPushButton("Allocate Memory")
        self.add_button.clicked.connect(self.allocate_process)
        self.layout.addWidget(self.add_button)

        self.frag_label = QLabel("Fragmentation: 0")
        self.layout.addWidget(self.frag_label)

        self.process_counter = 1
        self.update_scene()

    def allocate_process(self):
        try:
            size = int(self.input_size.text())
            if size <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a positive integer for process size.")
            return

        strategy = self.algorithms[self.dropdown.currentText()]
        allocated = strategy(self.memory_blocks, f"P{self.process_counter}", size)
        if allocated:
            self.process_counter += 1
        else:
            QMessageBox.warning(self, "Allocation Failed", "Not enough memory for this process.")
        self.update_scene()

    def update_scene(self):
        self.scene.clear()
        y = 0
        height_scale = 2
        for block in self.memory_blocks:
            height = block.size * height_scale
            rect = QGraphicsRectItem(QRectF(50, y, 200, height))
            color = QColor("red") if block.occupied else QColor("lightgray")
            rect.setBrush(color)
            self.scene.addItem(rect)

            label = f"{block.process_id if block.occupied else 'Free'} ({block.size})"
            self.scene.addText(label).setPos(260, y)
            y += height

        # Calculate fragmentation
        fragmentation = calculate_fragmentation(self.memory_blocks)
        self.frag_label.setText(f"Fragmentation: {fragmentation:.2f}%")
