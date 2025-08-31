from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from gui.device_check_screen import DeviceCheckScreen

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anub1s - Welcome")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Anub1s")
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc = QLabel("Rooting Samsung devices has never been easier.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 18px;")

        start_btn = QPushButton("Start")
        start_btn.setFixedWidth(150)
        start_btn.clicked.connect(self.go_to_device_check)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(30)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def go_to_device_check(self):
        self.device_screen = DeviceCheckScreen()
        self.device_screen.show()
        self.close()
