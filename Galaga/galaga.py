import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPainter, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Galaga.Widgets import MainWidget, MultiPlayerWidget

class Menu(QMainWindow):
    def __init__(self):
        self.current = MainWidget.MainWindow()

    def ChangeWidget(self):
        if(MainWidget.MainWindow.btnsingleplayer.clicked):
            self.current = MainWidget.MainWindow()
        elif(MainWidget.MainWindow.btnmultiplayer.clicked):
            self.current = MultiPlayerWidget.MainWindow()
        else:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Menu()
    sys.exit(app.exec_())