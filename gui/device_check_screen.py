# gui/device_check_screen.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtCore import QTimer, Qt
from utils.adb_utils import get_device_info
from utils.twrp_scraper import download_twrp_image
from utils.flash_utils import flash_recovery_with_heimdall
from utils.adb_heimdall_manager import ensure_adb_and_heimdall


class DeviceCheckScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device_info = None

        self.init_ui()
        self.apply_styles()
        self.animation_timer = QTimer()
        self.animation_step = 0
        self.animation_timer.timeout.connect(self._animate_status)

        # Auto check ADB/Heimdall, then start device check
        self.status_label.setText("Checking tools...")
        QApplication.processEvents()

        tools_ok, msg = ensure_adb_and_heimdall()
        if not tools_ok:
            QMessageBox.critical(self, "Tool Error", msg)
            self.status_label.setText("ADB/Heimdall setup failed.")
            return

        self.check_device()

    def init_ui(self):
        self.setWindowTitle("Anub1s - Device Check")
        self.resize(500, 300)

        self.status_label = QLabel("Ready to check device", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)

        self.check_btn = QPushButton("🔍 Check Device", self)
        self.check_btn.clicked.connect(self.check_device)

        self.flash_twrp_btn = QPushButton("⚡ Flash TWRP Recovery", self)
        self.flash_twrp_btn.setEnabled(False)
        self.flash_twrp_btn.clicked.connect(self.flash_twrp)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.addWidget(self.status_label)
        layout.addWidget(self.check_btn)
        layout.addWidget(self.flash_twrp_btn)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QPushButton {
                background-color: #2d89ef;
                border: none;
                color: white;
                padding: 10px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #1b6acb;
            }

            QPushButton:disabled {
                background-color: #444;
                color: #aaa;
            }

            QLabel {
                font-size: 15px;
            }
        """)

    def _animate_status(self):
        dots = "." * (self.animation_step % 4)
        base_text = self.status_label.text().split('.')[0]
        self.status_label.setText(f"{base_text}{dots}")
        self.animation_step += 1

    def check_device(self):
        self.status_label.setText("Checking device")
        self.animation_step = 0
        self.animation_timer.start(400)
        self.check_btn.setEnabled(False)
        self.flash_twrp_btn.setEnabled(False)
        QApplication.processEvents()

        info = get_device_info()
        self.animation_timer.stop()

        if not info:
            self.status_label.setText("No device detected or not a Samsung device.")
            QMessageBox.warning(self, "Device Not Found", "Please connect a Samsung device with ADB enabled.")
            self.check_btn.setEnabled(True)
            return

        self.device_info = info
        model = info.get("device", "Unknown")
        chipset = info.get("chipset", "Unknown")
        oneui_ver = info.get("oneui_version", "")

        self.status_label.setText(f"✅ Detected: {model} | Chipset: {chipset}")

        try:
            if int(oneui_ver) >= 800000:
                QMessageBox.information(self, "Bootloader", "Bootloader unlock not supported on this OneUI version.")
        except Exception:
            pass

        self.flash_twrp_btn.setEnabled(True)
        self.check_btn.setEnabled(True)

    def flash_twrp(self):
        if not self.device_info:
            QMessageBox.warning(self, "Error", "No device info available. Please check device first.")
            return

        self.flash_twrp_btn.setEnabled(False)
        self.check_btn.setEnabled(False)
        self.status_label.setText("📥 Downloading TWRP recovery...")

        QApplication.processEvents()

        img_path = download_twrp_image(self.device_info.get("device"), variant="stable")
        if not img_path:
            self.status_label.setText("❌ TWRP not found.")
            QMessageBox.warning(self, "Not Found", "TWRP recovery not found for this model.")
            self.flash_twrp_btn.setEnabled(True)
            self.check_btn.setEnabled(True)
            return

        self.status_label.setText("⚡ Flashing recovery via Heimdall... Please wait.")
        QApplication.processEvents()

        success, message = flash_recovery_with_heimdall(img_path)
        if success:
            QMessageBox.information(self, "Success", message)
            self.status_label.setText("✅ TWRP flashed successfully!")
        else:
            QMessageBox.warning(self, "Failed", message)
            self.status_label.setText("❌ Flash failed.")

        self.flash_twrp_btn.setEnabled(True)
        self.check_btn.setEnabled(True)

