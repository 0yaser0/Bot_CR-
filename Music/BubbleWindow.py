from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class BubbleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 500)
        self.initUI()

    def initUI(self):
        label = QLabel("This is the bubble window!", self)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, 300, 500)
        label.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
            color: black;
            font-size: 20px;
            padding: 20px;
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)
