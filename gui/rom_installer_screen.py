from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QComboBox, QLineEdit, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import subprocess
import requests
import os
from utils.rom_list import get_official_roms_for_device

def show_rom_installer_screen(device_model=None):
    window = QWidget()
    window.setWindowTitle("Anub1s - Install Custom ROM")
    window.setFixedSize(600, 500)
    window.setStyleSheet("background-color: #121212; color: white;")

    layout = QVBoxLayout()

    title = QLabel("Install Custom ROM")
    title.setFont(QFont("Arial", 20))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    # OFFICIAL
    layout.addSpacing(10)
    label1 = QLabel("📥 Install Official ROM")
    label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label1)

    rom_selector = QComboBox()
    rom_selector.setStyleSheet("background-color: white; color: black;")
    if device_model:
        roms = get_official_roms_for_device(device_model)
        for rom in roms:
            rom_selector.addItem(rom["name"], userData=rom["url"])
    layout.addWidget(rom_selector)

    btn_official = QPushButton("Download & Sideload Official ROM")
    btn_official.clicked.connect(lambda: handle_official_sideload(rom_selector))
    layout.addWidget(btn_official, alignment=Qt.AlignmentFlag.AlignCenter)

    # UNOFFICIAL
    layout.addSpacing(20)
    label2 = QLabel("🌐 Install Unofficial ROM (URL)")
    label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label2)

    url_input = QLineEdit()
    url_input.setPlaceholderText("Enter direct .zip URL")
    layout.addWidget(url_input)

    btn_unofficial = QPushButton("Download & Sideload Unofficial ROM")
    btn_unofficial.clicked.connect(lambda: handle_unofficial_sideload(url_input.text()))
    layout.addWidget(btn_unofficial, alignment=Qt.AlignmentFlag.AlignCenter)

    window.setLayout(layout)
    window.show()

def handle_official_sideload(combo):
    url = combo.currentData()
    name = combo.currentText()
    if not url:
        QMessageBox.critical(None, "Error", "No ROM selected.")
        return

    sideload_from_url(url, name)

def handle_unofficial_sideload(url):
    if not url or not url.endswith(".zip"):
        QMessageBox.critical(None, "Error", "Invalid URL or file format. Must end with .zip")
        return
    sideload_from_url(url, "Unofficial_ROM")

def sideload_from_url(url, name="rom"):
    os.makedirs("downloads", exist_ok=True)
    local_path = os.path.join("downloads", f"{name}.zip")

    try:
        print(f"Downloading ROM: {url}")
        r = requests.get(url, stream=True)
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print("Download complete.")

        subprocess.call(["adb", "reboot", "recovery"])
        input("In recovery? Select 'ADB sideload' then press Enter...")
        subprocess.call(["adb", "sideload", local_path])

    except Exception as e:
        QMessageBox.critical(None, "Download Error", f"Failed to download ROM:\n{e}")
