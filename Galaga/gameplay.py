import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time
import threading


class Gameplay(QWidget, QObject):

    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(Gameplay, self).__init__(parent)
        thread = threading.Thread(target=self.moveEnemies)
        # make test_loop terminate when the user exits the window
        thread.daemon = True

        self.resize(QSize(800, 600))
        self.list = []
        self.initUI()
        thread.start()

    def initUI(self):
        self.labelAvatar = QLabel(self)
        self.avatar = QPixmap("img/avatar.png")
        self.avatar = self.avatar.scaled(50, 50)
        self.labelAvatar.setPixmap(self.avatar)
        self.labelAvatar.move(10, 540)
        for i in range(0, 10):
            for j in range(0, 3):
                self.labelEnemy = QLabel(self)
                self.enemy = QPixmap("img/enemy.png")
                self.enemy = self.enemy.scaled(50, 50)
                self.labelEnemy.setPixmap(self.enemy)
                self.labelEnemy.move(150 + i*50, 10 + j*50)
                self.list.append(self.labelEnemy)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('PyGalaga')
        self.show()

    def startThread(self):
        self.thread.start()

    @pyqtSlot()
    def moveEnemies(self):
        direction = "left"
        while True:
            if direction == "left":
                for i in range(30):
                    self.list[i].move(self.list[i].x() - 10, self.list[i].y())
                if self.list[0].x() == 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    self.list[i].move(self.list[i].x() + 10, self.list[i].y())
                if self.list[29].x() == 740:
                    direction = "left"
            time.sleep(0.2)