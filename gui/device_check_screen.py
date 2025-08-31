from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from utils.adb_utils import get_device_info
from utils.flash_utils import flash_recovery_img
from utils.twrp_scraper import download_twrp_image
from gui.animations import fade_in, fade_out
from gui.rom_installer_screen import RomInstallerScreen

class DeviceCheckThread(QThread):
    device_info_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def run(self):
        info = get_device_info()
        if info:
            self.device_info_signal.emit(info)
        else:
            self.error_signal.emit("No Samsung device detected. Please connect a Samsung device with ADB enabled.")

class DeviceCheckScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anub1s - Device Check")
        self.setFixedSize(600, 450)
        self.setStyleSheet("""
            background-color: #121212;
            color: #eeeeee;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        """)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.status_label = QLabel("Detecting device...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.status_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate progress
        self.layout.addWidget(self.progress)

        self.device_info_label = QLabel("")
        self.device_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_info_label.setWordWrap(True)
        self.device_info_label.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.device_info_label)

        self.flash_twrp_btn = QPushButton("Flash TWRP Recovery")
        self.flash_twrp_btn.setFixedWidth(250)
        self.flash_twrp_btn.setEnabled(False)
        self.flash_twrp_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border-radius: 8px;
                padding: 12px 20px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
            QPushButton:hover:!disabled {
                background-color: #1565C0;
            }
        """)
        self.flash_twrp_btn.clicked.connect(self.flash_twrp)

        self.next_btn = QPushButton("Next: Install ROM")
        self.next_btn.setFixedWidth(250)
        self.next_btn.setEnabled(False)
        self.next_btn.setStyleSheet(self.flash_twrp_btn.styleSheet())
        self.next_btn.clicked.connect(self.go_to_rom_installer)

        self.layout.addWidget(self.flash_twrp_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

        self.device_info = None

        self.check_thread = DeviceCheckThread()
        self.check_thread.device_info_signal.connect(self.on_device_detected)
        self.check_thread.error_signal.connect(self.on_error)
        self.check_thread.start()

    def on_device_detected(self, info):
        self.progress.setRange(0, 1)
        self.status_label.setText("Device detected!")
        self.device_info = info

        info_text = (
            f"Model: {info.get('device')}\n"
            f"Chipset: {info.get('chipset')}\n"
            f"Android Version: {info.get('android_version')}\n"
            f"One UI Version: {info.get('oneui_version')}"
        )
        self.device_info_label.setText(info_text)
        self.flash_twrp_btn.setEnabled(True)
        self.next_btn.setEnabled(True)

    def on_error(self, message):
        self.progress.setRange(0, 1)
        self.status_label.setText("Error")
        self.device_info_label.setText(message)
        self.flash_twrp_btn.setEnabled(False)
        self.next_btn.setEnabled(False)

    def flash_twrp(self):
        if not self.device_info:
            QMessageBox.warning(self, "Error", "Device info not available.")
            return

        self.flash_twrp_btn.setEnabled(False)
        self.status_label.setText("Downloading TWRP recovery...")

        img_path = download_twrp_image(self.device_info.get("device"), variant="stable")
        if not img_path:
            QMessageBox.warning(self, "Error", "TWRP image not found for your device.")
            self.status_label.setText("Device detected!")
            self.flash_twrp_btn.setEnabled(True)
            return

        self.status_label.setText("Flashing TWRP recovery...")
        success = flash_recovery_img(img_path)
        if success:
            QMessageBox.information(self, "Success", "TWRP recovery flashed successfully.")
            self.status_label.setText("Device detected!")
        else:
            QMessageBox.warning(self, "Failed", "Failed to flash TWRP recovery.")
            self.status_label.setText("Device detected!")
        self.flash_twrp_btn.setEnabled(True)

    def go_to_rom_installer(self):
        self.rom_installer = RomInstallerScreen(self.device_info)
        fade_out(self)
        fade_in(self.rom_installer)

