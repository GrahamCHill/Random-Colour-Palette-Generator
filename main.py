from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import random
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class PaletteGenerator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palette Generator")
        self.setGeometry(100, 100, 800, 600)

        self.loaded_colors = []
        self.current_palette = []
        self.init_ui()

    def init_ui(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        load_action = QtWidgets.QAction("Load Palette (.dat)", self)
        load_action.triggered.connect(self.load_palette)
        file_menu.addAction(load_action)

        save_action = QtWidgets.QAction("Save Screenshot", self)
        save_action.triggered.connect(self.save_screenshot)
        file_menu.addAction(save_action)

        # Controls
        control_layout = QtWidgets.QHBoxLayout()

        self.count_spin = QtWidgets.QSpinBox()
        self.count_spin.setRange(1, 7)
        self.count_spin.setValue(5)
        control_layout.addWidget(QtWidgets.QLabel("Colors:"))
        control_layout.addWidget(self.count_spin)

        self.source_combo = QtWidgets.QComboBox()
        self.source_combo.addItems(["Loaded Palette Only"])
        control_layout.addWidget(QtWidgets.QLabel("Source:"))
        control_layout.addWidget(self.source_combo)

        self.generate_button = QtWidgets.QPushButton("Generate Palette")
        self.generate_button.clicked.connect(self.generate_palette)
        control_layout.addWidget(self.generate_button)

        layout.addLayout(control_layout)

        # Display area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.palette_widget = QtWidgets.QWidget()
        self.palette_layout = QtWidgets.QHBoxLayout(self.palette_widget)
        self.palette_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.scroll_area.setWidget(self.palette_widget)
        layout.addWidget(self.scroll_area)

    def load_palette(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load .dat Palette", "", "Palette Files (*.dat)")
        if not path:
            return
        with open(path, 'r') as f:
            for line in f:
                try:
                    name, hexcode = line.strip().split(',')
                    if hexcode.startswith('#') and len(hexcode) == 7:
                        self.loaded_colors.append((name.strip(), hexcode.strip()))
                except:
                    continue

    def generate_palette(self):
        count = self.count_spin.value()
        source_mode = self.source_combo.currentText()

        available_colors = self.loaded_colors.copy()

        if len(available_colors) < count:
            QtWidgets.QMessageBox.warning(self, "Not enough colors", "Not enough colors to generate the requested palette.")
            return

        self.current_palette = random.sample(available_colors, count)
        self.display_palette()

    def display_palette(self):
        # Clear layout
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for name, hexcode in self.current_palette:
            color_box = QtWidgets.QFrame()
            color_box.setFixedSize(100, 150)
            color_box.setStyleSheet(f"background-color: {hexcode}; border: 1px solid black;")

            label = QtWidgets.QLabel(f"{name}\n{hexcode}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)

            container = QtWidgets.QVBoxLayout()
            wrap = QtWidgets.QWidget()
            wrap.setLayout(container)
            container.addWidget(color_box)
            container.addWidget(label)

            self.palette_layout.addWidget(wrap)

    def save_screenshot(self):
        if not self.current_palette:
            return

        width = 150 * len(self.current_palette)
        height = 200
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()

        for i, (name, hexcode) in enumerate(self.current_palette):
            x = i * 150
            draw.rectangle([x, 0, x + 150, 150], fill=hexcode)
            draw.text((x + 10, 155), name, fill="black", font=font)
            draw.text((x + 10, 170), hexcode, fill="black", font=font)

        filename = f"palette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(filename)
        QtWidgets.QMessageBox.information(self, "Saved", f"Palette saved as {filename}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PaletteGenerator()
    window.show()
    sys.exit(app.exec_())
