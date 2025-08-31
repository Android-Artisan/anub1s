from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from gui.device_check_screen import show_device_check_screen
import sys

def run_app():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Anub1s")
    window.setFixedSize(600, 400)
    window.setStyleSheet("background-color: #121212; color: white;")

    layout = QVBoxLayout()

    title = QLabel("Anub1s")
    title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    subtitle = QLabel("Rooting has never been easier.")
    subtitle.setFont(QFont("Arial", 16))
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

    button = QPushButton("Get Started")
    button.setStyleSheet("""
        QPushButton {
            background-color: #1f1f1f;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #333;
        }
    """)
    button.clicked.connect(lambda: show_device_check_screen(app, window))

    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addSpacing(20)
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    window.setLayout(layout)
    window.show()
    app.exec()
