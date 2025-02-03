import sys
from PyQt5.QtWidgets import QApplication
from Music.CircularIcon import CircularIconWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularIconWindow()
    window.show()
    sys.exit(app.exec_())
