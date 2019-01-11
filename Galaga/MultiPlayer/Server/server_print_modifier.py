from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from Galaga.Scripts.my_thread import MyThread
from Galaga.Scripts.avatar import Avatar


class ServerPrintModifier(QWidget):

    move_p = pyqtSignal(QLabel)
    move_enemy_p = pyqtSignal(QLabel)
    count_enemy_signal = pyqtSignal()
    remove_enemy_projectile_signal = pyqtSignal()
    remove_player_projectile_signal = pyqtSignal()

    def __init__(self, avatar_num, server, parent=None):
        QWidget.__init__(self, parent)
        self.local_enemy_list = []
        self.server_modifier = server
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

    @pyqtSlot(int)
    def print_projectile(self, avatar_id):
        avatar = self.label_avatar[avatar_id]
        if avatar.isVisible():
            MyThread.mutex.acquire()
            pew = QPixmap("img/projectile.png")
            pew = pew.scaled(10, 10)
            self.projectile_label = QLabel(self)
            self.projectile_label.setPixmap(pew)
            self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
            self.projectile_label.show()
            self.projectile_list.append(self.projectile_label)
            self.move_p.emit(self.projectile_label)
            command = 'command-{}-create_projectile'.format(avatar_id)
            self.server_modifier.send_command(command)
            MyThread.mutex.release()

    @pyqtSlot(int, int)
    def move_enemy(self, index, position):
        MyThread.mutex.acquire()
        self.local_enemy_list[index].move(position, self.local_enemy_list[index].y())
        command = 'command-{}:{}-move_enemy'.format(index, position)
        self.server_modifier.send_command(command)
        MyThread.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_projectile(self, projectile, position):
        MyThread.mutex.acquire()
        projectile.move(projectile.x(), position)
        command = 'command-{}:{}-move_projectile'.format(self.projectile_list.index(projectile), position)
        self.server_modifier.send_command(command)
        MyThread.mutex.release()

    @pyqtSlot(int, int, int)
    def enemy_move_attack(self, enemy_index, coord_x, coord_y):
        MyThread.mutex.acquire()
        enemy = self.local_enemy_list[enemy_index]
        enemy.move(enemy.x() + coord_x, enemy.y() + coord_y)
        command = 'command-{}:{}:{}-enemy_kamikaze'.format(enemy_index, enemy.x(), enemy.y())
        self.server_modifier.send_command(command)
        MyThread.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_player(self, player, i):
        MyThread.mutex.acquire()
        command = 'command-{}:{}-print_player'.format(player.index, i)
        self.server_modifier.send_command(command)
        player.move(i, player.y())
        MyThread.mutex.release()

    @pyqtSlot(int, bool)
    def return_enemy(self, enemy_index, destroyed):
        MyThread.mutex.acquire()
        if destroyed:
            self.local_enemy_list[enemy_index].hide()
            self.count_enemy_signal.emit()
            command = 'command-{}-remove_enemy'.format(enemy_index)
            self.server_modifier.send_command(command)
        if enemy_index == 0 or enemy_index == 1 or enemy_index == 2:
            neighbour = self.local_enemy_list[enemy_index + 3]
            enemy = self.local_enemy_list[enemy_index]
            enemy.move(neighbour.x() - 50, neighbour.y())
            command = 'command-{}:{}-move_enemy'.format(enemy.x(), enemy.y())
            self.server_modifier.send_command(command)
        else:
            neighbour = self.local_enemy_list[enemy_index - 3]
            enemy = self.local_enemy_list[enemy_index]
            enemy.move(neighbour.x() + 50, neighbour.y())
            command = 'command-{}:{}-move_enemy'.format(enemy.x(), enemy.y())
            self.server_modifier.send_command(command)
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
            self.move_enemy_p.emit(self.projectile_label)
            command = 'command-{}-enemy_projectile_attack'.format(enemy_index)
            self.server_modifier.send_command(command)
            MyThread.mutex.release()

    @pyqtSlot(QLabel, int)
    def move_enemy_projectile(self, projectile, position):
        MyThread.mutex.acquire()
        command = 'command-{}-move_projectile'.format(self.projectile_list.index(projectile))
        self.server_modifier.send_command(command)
        projectile.move(projectile.x(), position)
        MyThread.mutex.release()

    @pyqtSlot()
    def new_level(self):
        command = 'command-null-next_level'
        self.server_modifier.send_command(command)
        self.remove_enemy_projectile_signal.emit()
        self.remove_player_projectile_signal.emit()
        for bullet in self.projectile_list:
            bullet.hide()
        for enemy in self.local_enemy_list:
            enemy.show()

    @pyqtSlot(int)
    def remove_player(self, index):
        for avatar in self.label_avatar:
            if avatar.index == index:
                MyThread.mutex.acquire()
                avatar.hide()
                command = 'command-{}-remove_player'.format(avatar.index)
                self.server_modifier.send_command(command)
                MyThread.mutex.release()


    @pyqtSlot(QLabel)
    def remove_projectile(self, projectile):
        MyThread.mutex.acquire()
        projectile.hide()
        command = 'command-{}-remove_projectile'.format(self.projectile_list.index(projectile))
        self.server_modifier.send_command(command)
        self.projectile_list.remove(projectile)
        MyThread.mutex.release()

    @pyqtSlot(QLabel)
    def remove_enemy(self, enemy):
        MyThread.mutex.acquire()
        enemy.hide()
        command = 'command-{}-remove_enemy'.format(self.local_enemy_list.index(enemy))
        self.server_modifier.send_command(command)
        self.count_enemy_signal.emit()
        MyThread.mutex.release()

