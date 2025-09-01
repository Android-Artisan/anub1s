from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtCore import QTimer, Qt
from utils.adb_utils import get_device_info
from utils.twrp_scraper import download_twrp_tar
from utils.flash_utils import flash_recovery_with_heimdall, reboot_to_download_mode

from utils.adb_heimdall_manager import get_heimdall_path, ensure_adb_and_heimdall
from gui.animations import fade_in, fade_out


class DeviceCheckScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device_info = None
        self.cached_tar_path = None

        self.init_ui()
        self.apply_styles()
        self.animation_timer = QTimer()
        self.animation_step = 0
        self.animation_timer.timeout.connect(self._animate_status)

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

        self.download_twrp_btn = QPushButton("⬇️ Download TWRP Recovery", self)
        self.download_twrp_btn.setEnabled(False)
        self.download_twrp_btn.clicked.connect(self.download_twrp)

        self.flash_twrp_btn = QPushButton("⚡ Flash TWRP Recovery", self)
        self.flash_twrp_btn.setEnabled(False)
        self.flash_twrp_btn.clicked.connect(self.flash_twrp)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        layout.addWidget(self.status_label)
        layout.addWidget(self.check_btn)
        layout.addWidget(self.download_twrp_btn)
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
        self.download_twrp_btn.setEnabled(False)
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

        self.check_btn.setEnabled(True)
        self.download_twrp_btn.setEnabled(True)
        self.flash_twrp_btn.setEnabled(self.cached_tar_path is not None)

    def download_twrp(self):
        if not self.device_info:
            QMessageBox.warning(self, "Error", "No device info available. Please check device first.")
            return
        if not self.device_info:
            QMessageBox.warning(self, "Error", "No device info detected.")
            return
        model = self.device_info.get("device")
        if not model:
            QMessageBox.warning(self, "Error", "Device model not found.")
            return
        if self.cached_tar_path:
            self.status_label.setText(f"TWRP already downloaded: {self.cached_tar_path}")
            self.flash_twrp_btn.setEnabled(True)
        else:
            self.status_label.setText(f"Downloading TWRP for {model}...")
            QApplication.processEvents()
            from utils.twrp_scraper import download_twrp_tar
            tar_path = download_twrp_tar(model)
            if tar_path:
                self.cached_tar_path = tar_path
                self.status_label.setText(f"TWRP downloaded: {tar_path}")
                self.flash_twrp_btn.setEnabled(True)
            else:
                self.status_label.setText("TWRP download failed.")
                QMessageBox.warning(self, "Download Failed", "Could not download TWRP for this device.")
        # Reboot to download mode only after a successful download (or if already downloaded)
        if self.cached_tar_path:
            from utils.flash_utils import reboot_to_download_mode
            rebooted = reboot_to_download_mode()
            if rebooted:
                QMessageBox.information(self, "Rebooted", "Device is rebooting to download mode. Please confirm when device is in download mode to continue flashing.")
            else:
                QMessageBox.warning(self, "Reboot Failed", "Could not reboot device to download mode. Please do it manually.")
        self.download_twrp_btn.setEnabled(False)
        self.check_btn.setEnabled(False)
        self.flash_twrp_btn.setEnabled(False)
        self.status_label.setText("📥 Downloading TWRP recovery tar...")
        QApplication.processEvents()

        device_model = self.device_info.get("device")
        tar_path = download_twrp_tar(device_model)

        if not tar_path:
            self.status_label.setText("❌ TWRP recovery tar not found or failed to download.")
            QMessageBox.warning(self, "Not Found", "TWRP recovery tar not found or failed to download.")
            self.download_twrp_btn.setEnabled(True)
            self.check_btn.setEnabled(True)
            return

        from gui.rom_installer_screen import RomInstallerScreen
        if not self.device_info:
            QMessageBox.warning(self, "Error", "No device info available.")
            return
        self.rom_installer = RomInstallerScreen(self.device_info)
        fade_out(self)
        fade_in(self.rom_installer)
        self.cached_tar_path = tar_path
        self.status_label.setText(f"✅ Downloaded and cached TWRP tar for {device_model}.")
        QMessageBox.information(self, "Downloaded", "TWRP tar downloaded successfully.\n\nNow you can flash it using the Flash button.")
        self.download_twrp_btn.setEnabled(False)
        self.flash_twrp_btn.setEnabled(True)
        self.check_btn.setEnabled(True)

    def flash_twrp(self):
        if not self.cached_tar_path:
            QMessageBox.warning(self, "Error", "No TWRP recovery tar cached. Please download it first.")
            return
        if not self.cached_tar_path:
            QMessageBox.warning(self, "Error", "No TWRP tar file downloaded.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Download Mode",
            "Is your device in download mode?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            self.status_label.setText("Please put your device in download mode and try again.")
            return
        from utils.flash_utils import get_heimdall_path, flash_recovery_with_heimdall
        heimdall_path = get_heimdall_path()
        if not heimdall_path:
            QMessageBox.warning(self, "Error", "Heimdall not found.")
            return
        self.status_label.setText("Flashing TWRP recovery...")
        QApplication.processEvents()
        success, msg = flash_recovery_with_heimdall(heimdall_path, self.cached_tar_path)
        if success:
            self.status_label.setText("TWRP flashed successfully!")
            QMessageBox.information(self, "Success", "TWRP recovery flashed successfully.")
        else:
            self.status_label.setText("TWRP flash failed.")
            QMessageBox.warning(self, "Flash Failed", f"TWRP flash failed: {msg}")
        self.flash_twrp_btn.setEnabled(False)
        self.check_btn.setEnabled(False)
        self.download_twrp_btn.setEnabled(False)
        self.status_label.setText("🔄 Rebooting device into Download Mode...")
        QApplication.processEvents()

        if not reboot_to_download_mode():
            self.status_label.setText("❌ Failed to reboot into Download Mode.")
            QMessageBox.warning(self, "Reboot Failed", "Failed to reboot device into Download Mode.")
            self.flash_twrp_btn.setEnabled(True)
            self.check_btn.setEnabled(True)
            self.download_twrp_btn.setEnabled(True)
            return

        heimdall_path = get_heimdall_path()
        if not heimdall_path:
            QMessageBox.critical(self, "Error", "Heimdall not found or failed to extract.")
            self.status_label.setText("Heimdall missing.")
            self.flash_twrp_btn.setEnabled(True)
            self.check_btn.setEnabled(True)
            self.download_twrp_btn.setEnabled(True)
            return

        self.status_label.setText("⚡ Flashing recovery via Heimdall... Please wait.")
        QApplication.processEvents()

        success, message = flash_recovery_with_heimdall(heimdall_path, self.cached_tar_path)
        if success:
            QMessageBox.information(self, "Success", message)
            self.status_label.setText("✅ TWRP flashed successfully!")
        else:
            QMessageBox.warning(self, "Failed", message)
            self.status_label.setText("❌ Flash failed.")

        self.flash_twrp_btn.setEnabled(True)
        self.check_btn.setEnabled(True)
        self.download_twrp_btn.setEnabled(True)

