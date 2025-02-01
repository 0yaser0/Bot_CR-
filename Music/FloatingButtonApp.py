import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QColor


class CircularIconWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the circular FAB window."""
        self.setupWindowProperties()
        self.loadBackgroundImage()
        self.setupCircularMask()
        self.setupDragVariables()
        self.bubble_shown = False
        self.bubble_window = None

    def setupWindowProperties(self):
        """Set window properties like size, flags, and transparency."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(70, 70)

    def loadBackgroundImage(self):
        """Load the background image for the FAB."""
        self.background_image = QPixmap("./assert/Logo_Bot_CR2.png")
        if self.background_image.isNull():
            print("Error: Unable to load the background image.")
            sys.exit(1)

    def setupCircularMask(self):
        """Make the window circular using a mask."""
        self.setMask(QRegion(0, 0, self.width(), self.height(), QRegion.Ellipse))

    def setupDragVariables(self):
        """Initialize variables for dragging the FAB."""
        self.dragging = False
        self.offset = QPoint()

    def paintEvent(self, event):
        """Override the paint event to draw the background color and image."""
        painter = QPainter(self)
        self.drawCircularBackground(painter)
        self.drawImage(painter)

    def drawCircularBackground(self, painter):
        """Draw the circular background color."""
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#2B9CB8"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())

    def drawImage(self, painter):
        """Draw the image within the circular bounds."""
        painter.setClipRegion(QRegion(self.rect(), QRegion.Ellipse))
        padding = 4
        image_rect = self.rect().adjusted(padding, padding, -padding, -padding)
        painter.drawPixmap(image_rect, self.background_image.scaled(image_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        """Handle mouse press event for dragging the FAB."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move event for dragging the FAB and bubble window."""
        if self.dragging:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            if self.bubble_shown:
                self.moveBubbleWindow(new_pos)

    def moveBubbleWindow(self, new_pos):
        """Move the bubble window along with the FAB."""
        bubble_x = new_pos.x() + (self.width() - self.bubble_window.width()) // 2
        bubble_y = new_pos.y() - self.bubble_window.height() + 35
        self.bubble_window.move(bubble_x, bubble_y)

    def mouseReleaseEvent(self, event):
        """Handle mouse release event to stop dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseDoubleClickEvent(self, event):
        """Handle double-click event to show/hide the bubble window."""
        if event.button() == Qt.LeftButton:
            if not self.bubble_shown:
                self.showBubble()
            else:
                self.hideBubble()

    def showBubble(self):
        """Show the bubble window."""
        self.bubble_window = BubbleWindow()
        self.setupBubbleWindow()
        self.bubble_shown = True

    def setupBubbleWindow(self):
        """Set up and position the bubble window."""
        self.bubble_window.setWindowFlags(Qt.FramelessWindowHint)
        self.bubble_window.setAttribute(Qt.WA_TranslucentBackground)
        self.positionBubbleWindow()
        self.bubble_window.show()
        self.raise_()  # Ensure the FAB stays on top

    def positionBubbleWindow(self):
        """Position the bubble window relative to the FAB."""
        bubble_width = self.bubble_window.width()
        bubble_height = self.bubble_window.height()
        fab_x = self.pos().x()
        fab_y = self.pos().y()
        bubble_x = fab_x + (self.width() - bubble_width) // 2
        bubble_y = fab_y - bubble_height + 35
        self.bubble_window.move(bubble_x, bubble_y)

    def hideBubble(self):
        """Hide the bubble window."""
        if self.bubble_window:
            self.bubble_window.close()
            self.bubble_window = None
        self.bubble_shown = False


class BubbleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the bubble window."""
        self.setFixedSize(300, 500)
        self.setupLabel()

    def setupLabel(self):
        """Set up the label inside the bubble window."""
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
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def mousePressEvent(self, event):
        """Override mouse press event to prevent the bubble from gaining focus."""
        pass  # Do nothing when the bubble is clicked


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularIconWindow()
    window.show()
    sys.exit(app.exec_())