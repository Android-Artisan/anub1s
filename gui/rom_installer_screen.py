from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QComboBox, QRadioButton, QButtonGroup, QHBoxLayout
)
from PyQt6.QtCore import Qt
from utils.download_utils import download_file
from utils.flash_utils import flash_zip_rom
from gui.animations import fade_in, fade_out

OFFICIAL_ROMS_JSON = "https://raw.githubusercontent.com/Android-Artisan/anub1s/refs/heads/main/official_roms.json"

import requests

class RomInstallerScreen(QWidget):
    def __init__(self, device_info):
        super().__init__()
        self.setWindowTitle("Anub1s - ROM Installer")
        self.setFixedSize(600, 450)
        self.setStyleSheet("""
            background-color: #121212;
            color: #eeeeee;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        """)

        self.device_info = device_info

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("Install Custom ROM")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(title)
        self.layout.addSpacing(20)

        self.rom_type_label = QLabel("Choose ROM type:")
        self.rom_type_label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.rom_type_label)

        self.official_radio = QRadioButton("Official ROMs")
        self.unofficial_radio = QRadioButton("Unofficial ROMs")

        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.official_radio)
        self.radio_group.addButton(self.unofficial_radio)
        self.official_radio.setChecked(True)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.official_radio)
        radio_layout.addWidget(self.unofficial_radio)
        self.layout.addLayout(radio_layout)

        self.rom_combo = QComboBox()
        self.rom_combo.setFixedWidth(400)
        self.layout.addWidget(self.rom_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.url_label = QLabel("")
        self.url_label.setWordWrap(True)
        self.url_label.hide()
        self.layout.addWidget(self.url_label)

        self.install_btn = QPushButton("Install ROM")
        self.install_btn.setFixedWidth(200)
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border-radius: 8px;
                padding: 12px 20px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.install_btn.clicked.connect(self.install_rom)
        self.layout.addWidget(self.install_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

        self.official_radio.toggled.connect(self.on_rom_type_changed)
        self.rom_combo.currentIndexChanged.connect(self.on_rom_selected)

        self.roms = {}
        self.load_official_roms()

    def load_official_roms(self):
        self.rom_combo.clear()
        self.url_label.hide()
        self.install_btn.setEnabled(False)
        try:
            r = requests.get(OFFICIAL_ROMS_JSON, timeout=10)
            r.raise_for_status()
            data = r.json()
            model = self.device_info.get("device").upper().replace(" ", "")
            roms_for_device = data.get(model, [])
            self.roms = {rom['name']: rom['url'] for rom in roms_for_device}
            if not self.roms:
                self.rom_combo.addItem("No official ROMs available for your device.")
                self.install_btn.setEnabled(False)
            else:
                for name in self.roms.keys():
                    self.rom_combo.addItem(name)
                self.install_btn.setEnabled(True)
        except Exception as e:
            self.rom_combo.addItem("Failed to load official ROMs.")
            self.install_btn.setEnabled(False)

    def on_rom_type_changed(self, checked):
        if checked:
            # Official ROMs
            self.rom_combo.show()
            self.url_label.hide()
            self.load_official_roms()
        else:
            # Unofficial ROMs
            self.rom_combo.clear()
            self.url_label.setText("Please enter unofficial ROM URL in the input box below.")
            self.url_label.show()
            self.install_btn.setEnabled(True)

    def on_rom_selected(self, index):
        if self.official_radio.isChecked():
            name = self.rom_combo.currentText()
            url = self.roms.get(name)
            if url:
                self.url_label.setText(f"Download URL:\n{url}")
                self.url_label.show()
            else:
                self.url_label.hide()

    def install_rom(self):
        if self.official_radio.isChecked():
            rom_name = self.rom_combo.currentText()
            rom_url = self.roms.get(rom_name)
            if not rom_url:
                QMessageBox.warning(self, "Error", "Select a valid ROM.")
                return
        else:
            # For simplicity, no input box for unofficial URL yet
            QMessageBox.information(self, "Info", "Unofficial ROM installation not implemented yet.")
            return

        self.install_btn.setEnabled(False)
        self.status_dialog = QMessageBox(self)
        self.status_dialog.setWindowTitle("Downloading ROM")
        self.status_dialog.setText("Downloading ROM. Please wait...")
        self.status_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.status_dialog.show()

        local_zip = download_file(rom_url)
        self.status_dialog.hide()

        if not local_zip:
            QMessageBox.warning(self, "Error", "Failed to download ROM.")
            self.install_btn.setEnabled(True)
            return

        self.status_dialog = QMessageBox(self)
        self.status_dialog.setWindowTitle("Flashing ROM")
        self.status_dialog.setText("Flashing ROM. Please wait...")
        self.status_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.status_dialog.show()

        success = flash_zip_rom(local_zip)
        self.status_dialog.hide()

        if success:
            QMessageBox.information(self, "Success", "ROM installed successfully.")
        else:
            QMessageBox.warning(self, "Failed", "Failed to flash ROM.")

        self.install_btn.setEnabled(True)

