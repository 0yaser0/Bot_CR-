from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QRegion, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize


class BubbleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 500)
        self.customizeShape()
        self.initUI()

    def customizeShape(self):
        full_region = QRegion(self.rect())

        cutout_width = 70
        cutout_height = 70
        x = (self.width() - cutout_width) // 2
        y = self.height() - cutout_height + 35

        ellipse_region = QRegion(x, y, cutout_width, cutout_height, QRegion.Ellipse)
        top_half_rect = QRegion(x, y, cutout_width, cutout_height // 2)
        half_ellipse_region = ellipse_region.intersected(top_half_rect)

        custom_region = full_region.subtracted(half_ellipse_region)
        self.setMask(custom_region)

    def initUI(self):
        # Button dimensions and spacing
        btn_width = 70
        btn_height = 70  # Adjust size to better display icons
        spacing = 25
        total_width = btn_width * 3 + spacing * 2
        margin = (self.width() - total_width) // 2
        y_position = self.height() - btn_height - 40

        icon_size = QSize(40, 40)  # Set the icon size for each button

        # Add the search bar above the image
        self.search_bar = QLineEdit(self)
        self.search_bar.setGeometry(20, self.height() // 5 - 50, 240, 30)  # Position of the search bar
        self.search_bar.setPlaceholderText("Search...")  # Placeholder text
        self.search_bar.setStyleSheet("border: 1px solid #ccc; border-radius: 15px; padding: 5px;")

        # Add the centered image above the buttons
        self.image_label = QLabel(self)
        self.image_label.setGeometry(30, self.height() // 6, 250, 300)  # Image position and size
        self.image_label.setPixmap(QPixmap("./assert/img.png").scaled(200, 200, Qt.KeepAspectRatio))  # Add your image here
        self.image_label.setAlignment(Qt.AlignCenter)

        # Previous button with icon
        self.prev_button = QPushButton(self)
        self.prev_button.setGeometry(margin, y_position, btn_width, btn_height)
        self.prev_button.setIcon(QIcon("./assert/back.png"))
        self.prev_button.setIconSize(icon_size)
        self.prev_button.clicked.connect(self.on_prev)
        self.prev_button.setStyleSheet("border: none; background: transparent;")

        # Play button with icon
        self.play_button = QPushButton(self)
        self.play_button.setGeometry(margin + btn_width + spacing, y_position, btn_width, btn_height)
        self.play_button.setIcon(QIcon("./assert/play.png"))
        self.play_button.setIconSize(icon_size)
        self.play_button.clicked.connect(self.on_play)
        self.play_button.setStyleSheet("border: none; background: transparent;")

        # Next button with icon
        self.next_button = QPushButton(self)
        self.next_button.setGeometry(margin + (btn_width + spacing) * 2, y_position, btn_width, btn_height)
        self.next_button.setIcon(QIcon("./assert/next.png"))
        self.next_button.setIconSize(icon_size)
        self.next_button.clicked.connect(self.on_next)
        self.next_button.setStyleSheet("border: none; background: transparent;")

    def on_prev(self):
        print("Previous button clicked!")

    def on_play(self):
        print("Play button clicked!")

    def on_next(self):
        print("Next button clicked!")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the white bubble shape.
        painter.setBrush(QColor("#FFFFFF"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        # Draw centered text.
        painter.setPen(QColor("#000000"))
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)


# For testing the widget independently:
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = BubbleWindow()
    window.show()
    sys.exit(app.exec_())
