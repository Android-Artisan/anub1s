from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QRadioButton, QButtonGroup,
    QListWidget, QMessageBox, QLineEdit, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
from utils.rom_list import get_official_roms_for_device
from utils.flash_utils import flash_zip_rom
from utils.download_utils import download_file
import os
import threading

class RomInstallerScreen(QWidget):
    def __init__(self, device_model):
        super().__init__()
        self.setWindowTitle("Install Custom ROM")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.device_model = device_model

        layout = QVBoxLayout()

        self.info_label = QLabel(f"Device model: {device_model}")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        # Radio buttons
        self.radio_official = QRadioButton("Official ROM")
        self.radio_unofficial = QRadioButton("Unofficial ROM")
        self.radio_official.setChecked(True)

        radio_group = QButtonGroup()
        radio_group.addButton(self.radio_official)
        radio_group.addButton(self.radio_unofficial)

        layout.addWidget(self.radio_official)
        layout.addWidget(self.radio_unofficial)

        # Official ROM list
        self.rom_list = QListWidget()
        layout.addWidget(self.rom_list)

        # Unofficial input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter unofficial ROM download URL here")
        self.url_input.setDisabled(True)
        layout.addWidget(self.url_input)

        # Buttons
        self.install_btn = QPushButton("Install ROM")
        self.install_btn.clicked.connect(self.install_rom)
        layout.addWidget(self.install_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        # Signals for radio
        self.radio_official.toggled.connect(self.toggle_mode)

        self.load_official_roms()

    def toggle_mode(self):
        if self.radio_official.isChecked():
            self.rom_list.setEnabled(True)
            self.url_input.setDisabled(True)
        else:
            self.rom_list.setDisabled(True)
            self.url_input.setEnabled(True)

    def load_official_roms(self):
        roms = get_official_roms_for_device(self.device_model)
        self.rom_list.clear()
        if not roms:
            self.rom_list.addItem("(No official ROMs found for this device)")
            self.rom_list.setDisabled(True)
            return
        for rom in roms:
            item = QListWidgetItem(rom["name"])
            item.setData(Qt.ItemDataRole.UserRole, rom["url"])
            self.rom_list.addItem(item)

    def install_rom(self):
        if self.radio_official.isChecked():
            item = self.rom_list.currentItem()
            if not item or not item.data(Qt.ItemDataRole.UserRole):
                QMessageBox.warning(self, "Select ROM", "Please select a ROM from the list.")
                return
            url = item.data(Qt.ItemDataRole.UserRole)
            # Download and flash in thread to avoid blocking
            threading.Thread(target=self.download_and_flash, args=(url,), daemon=True).start()
        else:
            url = self.url_input.text().strip()
            if not url:
                QMessageBox.warning(self, "Input URL", "Please enter a ROM download URL.")
                return
            threading.Thread(target=self.download_and_flash, args=(url,), daemon=True).start()

    def download_and_flash(self, url):
        self.install_btn.setDisabled(True)
        self.install_btn.setText("Downloading...")
        try:
            # Download zip to temp folder
            local_path = download_file(url)
            if not local_path:
                raise Exception("Download failed.")
            self.install_btn.setText("Flashing...")
            # Flash zip ROM via ADB sideload or custom method
            flash_zip_rom(local_path)
            self.install_btn.setText("Done!")
            QMessageBox.information(self, "Success", "ROM installed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to install ROM:\n{e}")
        finally:
            self.install_btn.setEnabled(True)
            self.install_btn.setText("Install ROM")
