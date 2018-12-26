import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Gameplay(QWidget):
    def __init__(self, parent=None):
        super(Gameplay, self).__init__(parent)
        self.labelAvatar1 = QLabel(self)
        self.labelAvatar2 = QLabel(self)
        self.resize(QSize(800, 600))
        self.initUI()

    def initUI(self):

        avatar1 = QPixmap("img/avatar.png")
        avatar1 = avatar1.scaled(50, 50)
        self.labelAvatar1.setPixmap(avatar1)
        self.labelAvatar1.move(10, 540)

        avatar2 = QPixmap("img/avatar.png")
        avatar2 = avatar1.scaled(50, 50)
        self.labelAvatar2.setPixmap(avatar2)
        self.labelAvatar2.move(740, 540)

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

        avatar1 = self.labelAvatar1
        avatar2 = self.labelAvatar2
        key = event.key()

        if key == Qt.Key_Left:
            if avatar1.x() > 10:
                avatar1.move(avatar1.x() - 10, avatar1.y())

        elif key == Qt.Key_Right:
            if avatar1.x() < 740:
                avatar1.move(avatar1.x() + 10, avatar1.y())

        if key == Qt.Key_A:
            if avatar2.x() > 10:
                avatar2.move(avatar2.x() - 10, avatar2.y())

        elif key == Qt.Key_D:
            if avatar2.x() < 740:
                avatar2.move(avatar2.x() + 10, avatar2.y())
