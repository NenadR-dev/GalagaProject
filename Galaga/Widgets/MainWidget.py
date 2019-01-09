import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPainter, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.resize(QSize(800, 600))


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 800, 600)
        self.setFixedSize(800, 600)
        self.startUIWindow()
        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("PyGalaga")
        self.setWindowIcon(QIcon("img/avatar1.png"))
        self.btnsingleplayer = QPushButton('Single Player', self)
        self.btnsingleplayer.move(350, 100)

        self.btnmultiplayer = QPushButton('Multi Player', self)
        self.btnmultiplayer.move(350, 300)

        self.btnexit = QPushButton("Exit", self)
        self.btnexit.move(350, 500)
        self.btnexit.clicked.connect(self.ExitGame)
        self.show()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def ExitGame(self):
        self.close()
