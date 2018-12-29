from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from Galaga.Scripts.my_thread import MyThread


class PrintModifier(QWidget, MyThread):

    move_p = pyqtSignal(QLabel)
    move_enemy_p = pyqtSignal(QLabel)

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
        if len(self.local_enemy_list) > 0:
            self.local_enemy_list.clear() # Ubijeni vanzemaljci su samo sakriveni
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
        if avatar.isVisible():
            self.mutex.acquire()
            pew = QPixmap("img/projectile.png")
            pew = pew.scaled(10, 10)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            self.move_p.emit(self.projectile_label)
            self.mutex.release()

    @pyqtSlot(int, int)
    def move_player(self, player, i):
        if player == 1:
            self.mutex.acquire()
            self.label_avatar1.move(i, self.label_avatar1.y())
            self.mutex.release()
        elif player == 2:
            self.mutex.acquire()
            self.label_avatar2.move(i, self.label_avatar2.y())
            self.mutex.release()

    @pyqtSlot(int, int)
    def move_enemy(self, index, position):
        self.mutex.acquire()
        self.local_enemy_list[index].move(position, self.local_enemy_list[index].y())
        self.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_projectile(self, projectile, position):
        self.mutex.acquire()
        projectile.move(projectile.x(), position)
        self.mutex.release()

    @pyqtSlot(int, int, int)
    def enemy_move_attack(self, enemy_index, coord_x, coord_y):
        self.mutex.acquire()
        enemy = self.local_enemy_list[enemy_index]
        enemy.move(enemy.x() + coord_x, enemy.y() + coord_y)
        self.mutex.release()

    @pyqtSlot(int)
    def return_enemy(self, enemy_index):
        self.mutex.acquire()
        if enemy_index == 0 or enemy_index == 1 or enemy_index == 2:
            neighbour = self.local_enemy_list[enemy_index + 3]
            enemy = self.local_enemy_list[enemy_index]
            enemy.move(neighbour.x() - 50, neighbour.y())
        else:
            neighbour = self.local_enemy_list[enemy_index - 3]
            enemy = self.local_enemy_list[enemy_index]
            enemy.move(neighbour.x() + 50, neighbour.y())
        self.mutex.release()

    @pyqtSlot(int)
    def enemy_projectile_attack(self, enemy_index):
        enemy = self.local_enemy_list[enemy_index]
        if enemy.isVisible():
            self.mutex.acquire()
            pew = QPixmap("img/enemy_projectile.png")
            pew = pew.scaled(10, 10)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(enemy.x() + 20, enemy.y() + 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            self.move_enemy_p.emit(self.projectile_label)
            self.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_enemy_projectile(self, projectile, position):
        self.mutex.acquire()
        projectile.move(projectile.x(), position)
        self.mutex.release()

    @pyqtSlot()
    def new_level(self):
        # TODO Wait for all projectiles to be removed before new level
        """print(len(self.projectile_list))
        while len(self.projectile_list) > 0:
            time.sleep(0.5)
            pass"""
        self.print_enemies()

    @pyqtSlot(int)
    def remove_player(self, index):
        if index == 1:
            self.label_avatar1.hide()
        elif index == 2:
            self.label_avatar2.hide()

    @pyqtSlot(QLabel)
    def remove_projectile(self, projectile):
        self.projectile_list.remove(projectile)
