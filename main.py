from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import random
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Hyperpop color palette
BASE_COLORS = [
    # Core originals
    ("Electric Pink", "#FF00C8"),
    ("Toxic Lime", "#C8FF00"),
    ("Sky Slush Blue", "#00EFFF"),
    ("Chrome Lavender", "#D2A1FF"),
    ("Digital Grape", "#8000FF"),
    ("Retina Burn Red", "#FF1F1F"),
    ("Bubblegum White", "#FDFDFF"),
    ("Blacklight Void", "#0A0033"),
    ("Glitch Yellow", "#FFFB00"),
    ("Soft Cyan Dream", "#9EFFF7"),
    ("Neon Coral", "#FF6EFF"),
    ("Cyber Mint", "#99FFCC"),
    ("Blushcore", "#FF85A1"),
    ("Plastic Peach", "#FFD6F6"),

    # Additional aesthetic chaos
    ("Slime Vibe Green", "#00FF99"),
    ("Overdrive Orange", "#FF7700"),
    ("Nuclear Frost", "#CCFFFF"),
    ("Laser Lemon", "#FFFF33"),
    ("Candyblood Red", "#FF3366"),
    ("Tamagotchi Teal", "#00FFDD"),
    ("Cotton Candy Fog", "#FFCCFF"),
    ("Ice Pop Purple", "#CC99FF"),
    ("Sunshock Yellow", "#FFF700"),
    ("Synthetic Rose", "#FF007F"),
    ("Hyper Ice", "#B6F7FF"),
    ("Pixel Dust", "#F5E3FF"),
    ("8bit Blood", "#D90037"),
    ("Noise Turquoise", "#00FFE5"),
    ("Chroma Blast", "#FD00FF"),
    ("Acid Rain", "#BFFF00"),
    ("Meme Slime", "#00FFB2"),
    ("Overheat Orange", "#FF5500"),
    ("Ghost Glow", "#D0FFFF"),
    ("Bluetooth Blue", "#3399FF"),
    ("Lavender Circuit", "#E3B9FF"),
    ("Sugar Rush Pink", "#FFAACC"),
    ("Twitch Purple", "#9146FF"),
    ("Sour Byte", "#BFFFBA"),
    ("Pop Pixel Pink", "#FF66B2"),
    ("Ultra Cyan", "#00FFFF"),
    ("Synthetic Strawberry", "#FF4D6D"),
    ("Toxic Cotton", "#E6FFB8"),
    ("Pastel Battery", "#F6FFD7"),
    ("Corrosive Mango", "#FFB84D"),
    ("Electro Magenta", "#FF008C"),
    ("Radioactive Teal", "#00FFD1"),
    ("Hard Light Rose", "#F08080"),
    ("Skater Mint", "#D2FFE3"),
    ("Arcade Lava", "#FF4500"),
    ("Cursed Plasma", "#B300FF"),
    ("Blinding Fizz", "#FFFFE0"),
    ("Supernova Citrus", "#FFF200"),
    ("Heatwave Pink", "#FF5FA2"),
    ("Power Surge", "#FF00E6"),
    ("Artificial Lemonade", "#FCFF6C"),
    ("Unicorn Noise", "#FCE1FF"),
]



class PaletteGenerator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hyperpop Palette Generator")
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
        self.source_combo.addItems(["Base Palette Only", "Loaded Palette Only", "Mixed Palette"])
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

        if source_mode == "Base Palette Only":
            available_colors = BASE_COLORS.copy()
        elif source_mode == "Loaded Palette Only":
            available_colors = self.loaded_colors.copy()
        else:
            available_colors = BASE_COLORS + self.loaded_colors

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
