from PyQt6.QtWidgets import QApplication
import sys
from gui.welcome_screen import WelcomeScreen

def main():
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    welcome.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

