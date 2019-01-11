from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from Galaga.Scripts.my_thread import MyThread
from Galaga.Scripts.avatar import Avatar
import time, random


class PrintModifier(QWidget):

    move_p = pyqtSignal(QLabel)
    move_enemy_p = pyqtSignal(QLabel)
    count_enemy_signal = pyqtSignal()
    return_enemy_signal = pyqtSignal(bool)
    remove_enemy_projectile_signal = pyqtSignal()
    remove_player_projectile_signal = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.local_enemy_list = []
        self.label_avatar1 = Avatar(self)
        self.label_avatar2 = Avatar(self)
        self.resize(QSize(800, 600))
        self.projectile_list = []
        self.print_enemies()
        self.gifts = []
        self.gift = QLabel(self)
        self.gift_type = True
        self.in_attack_ids = []
        self.start_moving_enemy = True

    def print_enemies(self):
        if len(self.local_enemy_list) > 0:
            self.local_enemy_list.clear()     # Ubijeni vanzemaljci su samo sakriveni
        for i in reversed(range(0, 3)):
            for j in reversed(range(0, 10)):
                #MyThread.mutex.acquire()
                label_enemy = QLabel(self)
                enemy = QPixmap("img/enemy.png")
                enemy = enemy.scaled(50, 50)
                label_enemy.setPixmap(enemy)
                label_enemy.move(150 + j * 50, 10 + i * 50)
                label_enemy.show()
                self.local_enemy_list.append(label_enemy)
                #MyThread.mutex.release()

    @pyqtSlot(QLabel)
    def print_projectile(self, avatar):
        if avatar.isVisible():
            #MyThread.mutex.acquire()
            pew = QPixmap("img/projectile.png")
            pew = pew.scaled(10, 10)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            self.move_p.emit(self.projectile_label)
            #MyThread.mutex.release()

    @pyqtSlot(int, int)
    def move_enemy(self, index, position):
        #MyThread.mutex.acquire()
        if self.start_moving_enemy:
            self.local_enemy_list[index].move(position, self.local_enemy_list[index].y())
        else:
            time.sleep(3)       #todo treba da se zaustave enemies
            self.start_moving_enemy = True
        #MyThread.mutex.release()

    @pyqtSlot(bool)
    def can_move_enemy(self, can_move):
        self.start_moving_enemy = can_move

    @pyqtSlot(QLabel, int)
    def move_projectile(self, projectile, position):
        #MyThread.mutex.acquire()
        projectile.move(projectile.x(), position)
        #MyThread.mutex.release()

    @pyqtSlot(int, int, int)
    def enemy_move_attack(self, enemy_index, coord_x, coord_y):
        #MyThread.mutex.acquire()
        if enemy_index not in self.in_attack_ids:
            self.in_attack_ids.append(enemy_index)
        enemy = self.local_enemy_list[enemy_index]
        enemy.move(enemy.x() + coord_x, enemy.y() + coord_y)
        #MyThread.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_player(self, player, i):
        #MyThread.mutex.acquire()
        player.move(i, player.y())
        #MyThread.mutex.release()

    @pyqtSlot(int, bool)
    def return_enemy(self, enemy_index, destroyed):
        #MyThread.mutex.acquire()
        self.in_attack_ids.remove(enemy_index)
        if destroyed:
            self.local_enemy_list[enemy_index].hide()
            self.count_enemy_signal.emit()

        if enemy_index == 29 or enemy_index == 19 or enemy_index == 9:
            i = 1
            neighbour = self.local_enemy_list[enemy_index - i]
            while (not (neighbour.y() - 10) % 50) and neighbour.y() <= 110:
                i += 1
                neighbour = self.local_enemy_list[enemy_index - i]
            enemy = self.local_enemy_list[enemy_index]
            enemy.move(neighbour.x() - 50, neighbour.y())
        else:
            neighbour = self.local_enemy_list[enemy_index + 1]
            enemy = self.local_enemy_list[enemy_index]
            enemy.move(neighbour.x() + 50, neighbour.y())
        #MyThread.mutex.release()

    @pyqtSlot(int)
    def enemy_projectile_attack(self, enemy_index):
        enemy = self.local_enemy_list[enemy_index]
        if enemy.isVisible():
            #MyThread.mutex.acquire()
            pew = QPixmap("img/new_enemy_projectile.png")
            pew = pew.scaled(20, 20)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(enemy.x() + 20, enemy.y() + 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            self.move_enemy_p.emit(self.projectile_label)
            #MyThread.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_enemy_projectile(self, projectile, position):
        #MyThread.mutex.acquire()
        projectile.move(projectile.x(), position)
        #MyThread.mutex.release()

    @pyqtSlot()
    def new_level(self):
        self.remove_enemy_projectile_signal.emit()
        self.remove_player_projectile_signal.emit()

        for bullet in self.projectile_list:
            bullet.hide()
        for id in self.in_attack_ids:
            self.return_enemy(id, False)
        for enemy in self.local_enemy_list:
            enemy.show()

    @pyqtSlot(int)
    def remove_player(self, index):
        if self.label_avatar1.index == index:
            #MyThread.mutex.acquire()
            self.label_avatar1.hide()
            #MyThread.mutex.release()

        elif self.label_avatar2.index == index:
            #MyThread.mutex.acquire()
            self.label_avatar2.hide()
            #MyThread.mutex.release()

    @pyqtSlot(QLabel)
    def remove_projectile(self, projectile):
        #MyThread.mutex.acquire()
        projectile.hide()
        self.projectile_list.remove(projectile)
        #MyThread.mutex.release()

    @pyqtSlot(QLabel)
    def remove_enemy(self, enemy):
        #MyThread.mutex.acquire()
        enemy.hide()
        self.count_enemy_signal.emit()
        #MyThread.mutex.release()

    @pyqtSlot()
    def print_gift(self):
        MyThread.mutex.acquire()
        if random.randint(0, 1):
            gift_img = QPixmap("img/present1.png")
            gift_img = gift_img.scaled(45, 45)
            self.gift.setPixmap(gift_img)
            x = random.randint(10, 740)
            self.gift.move(x, 540)
            self.gift.show()
            self.gifts.append(self.gift)
            self.gift_type = True
        else:
            gift_img = QPixmap("img/bad_present.png")
            gift_img = gift_img.scaled(45, 45)
            self.gift.setPixmap(gift_img)
            x = random.randint(10, 740)
            self.gift.move(x, 540)
            self.gift.show()
            self.gift_type = False
            self.gifts.append(self.gift)

        MyThread.mutex.release()

    @pyqtSlot()
    def remove_gift(self):
        MyThread.mutex.acquire()
        #self.gifts.remove(self.gift)
        self.gift.hide()
        MyThread.mutex.release()

