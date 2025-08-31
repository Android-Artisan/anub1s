from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from utils.adb_utils import get_device_info, unlock_bootloader
from utils.twrp_scraper import download_twrp_image
from utils.flash_utils import flash_recovery_img
from gui.rom_installer_screen import RomInstallerScreen

class DeviceCheckThread(QThread):
    device_info_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def run(self):
        info = get_device_info()
        if info:
            self.device_info_ready.emit(info)
        else:
            self.error_occurred.emit("No Samsung device detected or ADB not connected.")

class DeviceCheckScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anub1s - Device Info")
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.status_label = QLabel("Detecting Samsung device via ADB...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.info_labels = []
        self.unlock_btn = None
        self.flash_twrp_btn = None
        self.install_rom_btn = None

        self.setLayout(self.layout)

        # Start detection thread
        self.check_thread = DeviceCheckThread()
        self.check_thread.device_info_ready.connect(self.on_device_info)
        self.check_thread.error_occurred.connect(self.on_error)
        self.check_thread.start()

        self.device_info = None

    def on_device_info(self, info):
        self.device_info = info
        self.status_label.setText("Device detected successfully:")

        # Display device info
        for label in self.info_labels:
            self.layout.removeWidget(label)
            label.deleteLater()
        self.info_labels.clear()

        for key, val in info.items():
            lbl = QLabel(f"{key.capitalize()}: {val}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(lbl)
            self.info_labels.append(lbl)

        # Check One UI version for bootloader unlocking
        oneui = int(info["oneui"].replace(".", "").ljust(6, "0"))
        if oneui >= 800000:
            lock_msg = QLabel("⚠️ Bootloader unlocking not supported on One UI 8+.")
            lock_msg.setStyleSheet("color: red;")
            lock_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(lock_msg)
        else:
            self.unlock_btn = QPushButton("Unlock Bootloader")
            self.unlock_btn.clicked.connect(self.unlock_bootloader)
            self.layout.addWidget(self.unlock_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Flash TWRP button
        self.flash_twrp_btn = QPushButton("Download & Flash TWRP")
        self.flash_twrp_btn.clicked.connect(self.flash_twrp)
        self.layout.addWidget(self.flash_twrp_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Install ROM button
        self.install_rom_btn = QPushButton("Install Custom ROM")
        self.install_rom_btn.clicked.connect(self.install_rom)
        self.layout.addWidget(self.install_rom_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_error(self, msg):
        self.status_label.setText(msg)
        QMessageBox.critical(self, "Error", msg)

    def unlock_bootloader(self):
        ret = unlock_bootloader()
        if ret:
            QMessageBox.information(self, "Success", "Bootloader unlock command sent.")
        else:
            QMessageBox.warning(self, "Failed", "Bootloader unlock failed or not supported.")

    def flash_twrp(self):
        device_model = self.device_info.get("device")
        img_path = download_twrp_image(device_model)
        if not img_path:
            QMessageBox.warning(self, "Error", "TWRP image not found for your device.")
            return

        success = flash_recovery_img(img_path)
        if success:
            QMessageBox.information(self, "Success", "TWRP flashed successfully.")
        else:
            QMessageBox.warning(self, "Failed", "Flashing TWRP failed.")

    def install_rom(self):
        device_model = self.device_info.get("device")
        self.rom_screen = RomInstallerScreen(device_model)
        self.rom_screen.show()
        self.close()
