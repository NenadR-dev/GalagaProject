import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPainter, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
<<<<<<< HEAD
from Galaga.Widgets import MainWidget, MultiPlayerWidget
=======
from gameplay import Gameplay
>>>>>>> 0ebf5880fc3df6e23e99fe485b1e3f7f65407c2b

class Menu(QMainWindow):
    def __init__(self):
        self.current = MainWidget.MainWindow()

<<<<<<< HEAD
    def ChangeWidget(self):
        if(MainWidget.MainWindow.btnsingleplayer.clicked):
            self.current = MainWidget.MainWindow()
        elif(MainWidget.MainWindow.btnmultiplayer.clicked):
            self.current = MultiPlayerWidget.MainWindow()
        else:
            self.close()
=======
class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.resize(QSize(800, 600))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 800, 600)
        self.startUIWindow()

        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def startUIWindow(self):
        #self.Window = UIWindow(self)
        self.Window = Gameplay(self)
        self.setWindowTitle("PyGalaga")
        self.show()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)
>>>>>>> 0ebf5880fc3df6e23e99fe485b1e3f7f65407c2b


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Menu()
    sys.exit(app.exec_())