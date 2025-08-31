import sys
from PyQt6.QtWidgets import QApplication
from gui.welcome_screen import WelcomeScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    welcome_win = WelcomeScreen()
    welcome_win.show()

    sys.exit(app.exec())
