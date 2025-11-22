import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Data Analysis Platform")

    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()