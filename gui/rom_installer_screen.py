from PyQt6.QtWidgets import QWidget, QFileDialog, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import subprocess

def show_rom_installer_screen():
    window = QWidget()
    window.setWindowTitle("Anub1s - Install ROM")
    window.setFixedSize(600, 400)
    window.setStyleSheet("background-color: #121212; color: white;")

    layout = QVBoxLayout()

    title = QLabel("ROM Installer")
    title.setFont(QFont("Arial", 20))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    button = QPushButton("Choose ROM ZIP to Sideload")
    button.clicked.connect(lambda: select_and_sideload())
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    window.setLayout(layout)
    window.show()

def select_and_sideload():
    file_path, _ = QFileDialog.getOpenFileName(caption="Select ROM ZIP", filter="ZIP files (*.zip)")
    if file_path:
        subprocess.call(["adb", "reboot", "recovery"])
        input("Boot into recovery and select 'ADB sideload', then press Enter...")
        subprocess.call(["adb", "sideload", file_path])
