from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading
from Galaga.Scripts.my_thread import MyThread


class PrintModifier(QWidget, MyThread):

    move_p = pyqtSignal(QLabel)

    def __init__(self, parent=None):
        super(PrintModifier, self).__init__(parent)
        self.local_enemy_list = []
        self.label_avatar1 = QLabel(self)
        self.label_avatar2 = QLabel(self)
        self.resize(QSize(800, 600))
        self.projectile_list = []
        self.print_enemies()
        self.print_player()

    def print_enemies(self):
        for i in range(0, 10):
            for j in range(0, 3):
                self.mutex.acquire()
                label_enemy = QLabel(self)
                enemy = QPixmap("img/enemy.png")
                enemy = enemy.scaled(50, 50)
                label_enemy.setPixmap(enemy)
                label_enemy.move(150 + i * 50, 10 + j * 50)
                label_enemy.show()
                self.local_enemy_list.append(label_enemy)
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

    @pyqtSlot(QLabel)
    def print_projectile(self, avatar):
        self.mutex.acquire()
        pew = QPixmap("img/projectile.png")
        pew = pew.scaled(10, 10)
        self.projectile_label = QLabel(self)
        self.projectile_label.setPixmap(pew)
        self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
        self.projectile_label.show()
        self.move_p.emit(self.projectile_label)
        self.mutex.release()

    @pyqtSlot(int, int)
    def move_player(self, player, i):
        if player == 1:
            self.mutex.acquire()
            self.label_avatar1.move(i,self.label_avatar1.y())
            self.mutex.release()
        elif player == 2:
            self.mutex.acquire()
            self.label_avatar2.move(i,self.label_avatar2.y())
            self.mutex.release()

    def move_enemy(self, index, position):
        self.mutex.acquire()
        self.local_enemy_list[index].move(position, self.local_enemy_list[index].y())
        self.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_projectile(self, projectile, position):
        self.mutex.acquire()
        projectile.move(projectile.x(), position)
        self.mutex.release()