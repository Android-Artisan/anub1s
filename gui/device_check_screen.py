from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.adb_utils import get_device_info, unlock_bootloader
from utils.twrp_scraper import download_twrp_image
from utils.flash_utils import flash_recovery_img
from gui.rom_installer_screen import show_rom_installer_screen

def show_device_check_screen(app, previous_window):
    previous_window.close()

    window = QWidget()
    window.setWindowTitle("Anub1s - Device Info")
    window.setFixedSize(600, 500)
    window.setStyleSheet("background-color: #121212; color: white;")

    layout = QVBoxLayout()
    title = QLabel("Detecting Samsung Device...")
    title.setFont(QFont("Arial", 18))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    info = get_device_info()

    if info is None:
        error = QLabel("No Samsung device detected. Is ADB enabled?")
        error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(error)
    else:
        for key, val in info.items():
            lbl = QLabel(f"{key.capitalize()}: {val}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        oneui = int(info["oneui"].replace(".", "").ljust(6, "0"))
        if oneui >= 800000:
            lock_msg = QLabel("❌ Bootloader unlocking not supported on One UI 8+.")
            lock_msg.setStyleSheet("color: red;")
            lock_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lock_msg)
        else:
            unlock_btn = QPushButton("🔓 Unlock Bootloader")
            unlock_btn.clicked.connect(unlock_bootloader)
            layout.addWidget(unlock_btn, alignment=Qt.AlignmentFlag.AlignCenter)

            flash_btn = QPushButton("💾 Download & Flash TWRP")
            flash_btn.clicked.connect(lambda: flash_twrp(info["device"]))
            layout.addWidget(flash_btn, alignment=Qt.AlignmentFlag.AlignCenter)

            rom_btn = QPushButton("📦 Install ROM")
            rom_btn.clicked.connect(show_rom_installer_screen)
            layout.addWidget(rom_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    window.setLayout(layout)
    window.show()

def flash_twrp(device_model):
    img_path = download_twrp_image(device_model)
    if img_path:
        flash_recovery_img(img_path)
