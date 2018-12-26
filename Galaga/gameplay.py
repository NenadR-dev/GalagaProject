import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Gameplay(QWidget):
    def __init__(self, parent=None):
        super(Gameplay, self).__init__(parent)
        self.resize(QSize(800, 600))
        self.initUI()

    def initUI(self):
        labelAvatar = QLabel(self)
        avatar = QPixmap("img/avatar.png")
        avatar = avatar.scaled(50, 50)
        labelAvatar.setPixmap(avatar)
        labelAvatar.move(10, 540)

        for i in range(0, 10):
            for j in range(0, 3):
                labelEnemy = QLabel(self)
                enemy = QPixmap("img/enemy.png")
                enemy = enemy.scaled(50, 50)
                labelEnemy.setPixmap(enemy)
                labelEnemy.move(150 + i*50, 10 + j*50)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('PyGalaga')
        self.show()

    def keyPressEvent(self, event):

        avatar = self.labelAvatar
        key = event.key()

        if key == Qt.Key_Left:
            self.move(avatar.winfo_rootx() - 10)

        elif key == Qt.Key_Right:
            self.move(avatar.winfo_rootx() + 10)

        else:
            self.move(avatar.winfo_rootx())