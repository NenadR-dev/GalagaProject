from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from Galaga.Scripts.my_thread import MyThread
from Galaga.Scripts.avatar import Avatar


class ClientPrintModifier(QWidget):

    def __init__(self, avatar_num, parent=None):
        QWidget.__init__(self, parent)
        self.local_enemy_list = []
        self.label_avatar = []
        for i in range(avatar_num):
            self.label_avatar.append(Avatar(self))
        self.resize(QSize(800, 600))
        self.projectile_list = []
        self.print_enemies()

    def print_enemies(self):
        for i in range(0, 10):
            for j in range(0, 3):
                MyThread.mutex.acquire()
                label_enemy = QLabel(self)
                enemy = QPixmap("img/enemy.png")
                enemy = enemy.scaled(50, 50)
                label_enemy.setPixmap(enemy)
                label_enemy.move(150 + i * 50, 10 + j * 50)
                label_enemy.show()
                self.local_enemy_list.append(label_enemy)
                MyThread.mutex.release()

    @pyqtSlot(QLabel)
    def print_projectile(self, avatar):
        if avatar.isVisible():
            MyThread.mutex.acquire()
            pew = QPixmap("img/projectile.png")
            pew = pew.scaled(10, 10)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            MyThread.mutex.release()

    @pyqtSlot(int, int)
    def move_enemy(self, index, position):
        MyThread.mutex.acquire()
        self.local_enemy_list[index].move(position, self.local_enemy_list[index].y())
        MyThread.mutex.release()

    @pyqtSlot(int, int)
    def move_projectile(self, index, position):
        MyThread.mutex.acquire()
        self.projectile_list[index].move(self.projectile_list[index].x(), position)
        MyThread.mutex.release()

    @pyqtSlot(int, int, int)
    def enemy_move_attack(self, enemy_index, coord_x, coord_y):
        MyThread.mutex.acquire()
        enemy = self.local_enemy_list[enemy_index]
        enemy.move(enemy.x() + coord_x, enemy.y() + coord_y)
        MyThread.mutex.release()

    @pyqtSlot(int, int)
    def move_player(self, id, position):
        MyThread.mutex.acquire()
        self.label_avatar[id].move(position, self.label_avatar[id].y())
        MyThread.mutex.release()

    @pyqtSlot(int)
    def enemy_projectile_attack(self, enemy_index):
        enemy = self.local_enemy_list[enemy_index]
        if enemy.isVisible():
            MyThread.mutex.acquire()
            pew = QPixmap("img/new_enemy_projectile.png")
            pew = pew.scaled(20, 20)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(enemy.x() + 20, enemy.y() + 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            MyThread.mutex.release()

    @pyqtSlot()
    def new_level(self):
        for bullet in self.projectile_list:
            MyThread.mutex.acquire()
            bullet.hide()
            self.projectile_list.remove(bullet)
            MyThread.mutex.release()
        for enemy in self.local_enemy_list:
            enemy.show()

    @pyqtSlot(int)
    def remove_player(self, index):
        for avatar in self.label_avatar:
            if avatar.index == index:
                MyThread.mutex.acquire()
                avatar.hide()
                MyThread.mutex.release()

    @pyqtSlot(int)
    def remove_projectile(self, id):
        MyThread.mutex.acquire()
        self.projectile_list[id].hide()
        del self.projectile_list[id]
        MyThread.mutex.release()

    @pyqtSlot(int)
    def remove_enemy(self, id):
        MyThread.mutex.acquire()
        self.local_enemy_list[id].hide()
        MyThread.mutex.release()

