import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap


class Gameplay(QWidget):
    def __init__(self, parent=None):
        super(Gameplay, self).__init__(parent)
        self.resize(QSize(800, 600))
        self.initUI()

    def initUI(self):
        labelAvatar1 = QLabel(self)
        avatar1 = QPixmap("img/avatar.png")
        avatar1 = avatar1.scaled(50, 50)
        labelAvatar1.setPixmap(avatar1)
        labelAvatar1.move(10, 540)

        labelAvatar2 = QLabel(self)
        avatar2 = QPixmap("img/avatar.png")
        avatar2 = avatar1.scaled(50, 50)
        labelAvatar2.setPixmap(avatar1)
        labelAvatar2.move(740, 540)

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