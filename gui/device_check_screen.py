from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.adb_utils import get_device_info
from utils.twrp_scraper import search_twrp_download

def show_device_check_screen(app, previous_window):
    previous_window.close()
    window = QWidget()
    window.setWindowTitle("Anub1s - Device Info")
    window.setFixedSize(600, 400)
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
            lock_msg = QLabel("Bootloader unlocking not supported on One UI 8+.")
            lock_msg.setStyleSheet("color: red;")
            lock_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lock_msg)
        else:
            layout.addSpacing(20)
            flash_button = QPushButton("Find and Flash TWRP")
            flash_button.clicked.connect(lambda: search_twrp_download(info["model"]))
            layout.addWidget(flash_button, alignment=Qt.AlignmentFlag.AlignCenter)

    window.setLayout(layout)
    window.show()
