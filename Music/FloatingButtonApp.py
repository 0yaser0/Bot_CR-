import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QRegion

class CircularIconWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # No title bar, always on top
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.setFixedSize(70, 70)  # Size of the circular icon

        # Load the background image
        self.background_image = QPixmap("./assert/Logo_Bot_CR2.png")  # Replace with your image path
        if self.background_image.isNull():
            print("Error: Unable to load the background image.")
            sys.exit(1)

        # Make the window circular
        self.setMask(QRegion(0, 0, self.width(), self.height(), QRegion.Ellipse))

        # Variables for dragging
        self.dragging = False
        self.offset = QPoint()

        # Track if the bubble is shown
        self.bubble_shown = False
        self.bubble_window = None

    def paintEvent(self, event):
        """Override the paint event to draw the background image."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Smooth edges
        painter.setRenderHint(QPainter.SmoothPixmapTransform)  # Smooth image scaling

        # Draw the image within the circular bounds
        painter.setClipRegion(QRegion(self.rect(), QRegion.Ellipse))
        painter.drawPixmap(self.rect(), self.background_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseDoubleClickEvent(self, event):
        """Handle double-click event to show/hide the bubble window."""
        print("Double-click detected!")  # Debug print
        if event.button() == Qt.LeftButton:
            if not self.bubble_shown:
                self.showBubble()
            else:
                self.hideBubble()

    def showBubble(self):
        """Show the bubble window."""
        print("Showing bubble...")  # Debug print
        self.bubble_window = BubbleWindow()  # Create the bubble window
        self.bubble_window.show()  # Show the bubble window
        self.bubble_shown = True

    def hideBubble(self):
        """Hide the bubble window."""
        print("Hiding bubble...")  # Debug print
        if self.bubble_window:
            self.bubble_window.close()  # Close the bubble window
            self.bubble_window = None
        self.bubble_shown = False


class BubbleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # No title bar, always on top
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.setFixedSize(300, 500)  # Size of the bubble window

        # Position the bubble window near the circular icon
        icon_pos = QApplication.desktop().cursor().pos()  # Get the current cursor position
        self.move(icon_pos.x(), icon_pos.y())  # Position the bubble at the cursor
        print(f"Bubble position: {self.pos()}")  # Debug print

        # Add content to the bubble window (e.g., a label)
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
        """Override the paint event to draw a rounded rectangle."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Smooth edges
        painter.setBrush(Qt.white)  # Background color
        painter.setPen(Qt.NoPen)  # No border
        painter.drawRoundedRect(self.rect(), 20, 20)  # Rounded rectangle


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularIconWindow()
    window.show()
    sys.exit(app.exec_())