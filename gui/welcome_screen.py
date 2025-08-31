from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from gui.device_check_screen import DeviceCheckScreen
from gui.animations import fade_in, fade_out

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anub1s")
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            background-color: #121212;
            color: #eeeeee;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Anub1s")
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.desc_label = QLabel("Rooting Samsung devices has never been easier.")
        self.desc_label.setStyleSheet("font-size: 18px;")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_btn = QPushButton("Get Started")
        self.start_btn.setFixedWidth(200)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border-radius: 8px;
                padding: 12px 24px;
                color: white;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.start_btn.clicked.connect(self.go_to_device_check)

        layout.addWidget(self.title_label)
        layout.addSpacing(10)
        layout.addWidget(self.desc_label)
        layout.addSpacing(50)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def go_to_device_check(self):
        from gui.device_check_screen import DeviceCheckScreen

        self.device_screen = DeviceCheckScreen()
        fade_out(self)
        fade_in(self.device_screen)

