from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading
from Galaga.Scripts.move_modifier import MoveModifer


class PrintModifier(QWidget):

    def __init__(self, parent=None):
        super(PrintModifier, self).__init__(parent)
        self.local_enemy_list = []
        self.mutex = Lock()
        self.label_avatar1 = QLabel(self)
        self.label_avatar2 = QLabel(self)
        self.resize(QSize(800, 600))
        self.projectile_list = []
        self.print_enemies()
        self.print_player()

    def print_enemies(self):
        self.mutex.acquire()
        for i in range(0, 10):
            for j in range(0, 3):
                label_enemy = QLabel(self)
                enemy = QPixmap("img/enemy.png")
                enemy = enemy.scaled(50, 50)
                label_enemy.setPixmap(enemy)
                label_enemy.move(150 + i * 50, 10 + j * 50)
                label_enemy.show()
                self.local_enemy_list.append(label_enemy)
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('PyGalaga')
        self.mutex.release()

    def print_player(self):
        self.mutex.acquire()
        avatar1 = QPixmap("img/avatar.png")
        avatar1 = avatar1.scaled(50, 50)
        self.label_avatar1.setPixmap(avatar1)
        self.label_avatar1.move(10, 540)
        self.label_avatar1.show()

        avatar2 = QPixmap("img/avatar2.png")
        avatar2 = avatar2.scaled(50, 50)
        self.label_avatar2.setPixmap(avatar2)
        self.label_avatar2.move(740, 540)
        self.label_avatar2.show()
        self.mutex.release()

    def print_projectile(self, avatar, projectiles):
        self.mutex.acquire()
        pew = QPixmap("img/projectile.png")
        pew = pew.scaled(10, 10)
        self.projectile_label = QLabel(self)
        self.projectile_label.setPixmap(pew)
        self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
        projectiles.append(self.projectile_label)
        self.projectile_label.show()
        self.mutex.release()
