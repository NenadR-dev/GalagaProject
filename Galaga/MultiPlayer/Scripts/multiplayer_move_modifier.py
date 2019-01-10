from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel
import time
from Galaga.Scripts.my_thread import MyThread
from Galaga.Sockets.socket_send import *


class MultiplayerMoveModifer(QThread):

    create_projectile_signal = pyqtSignal(QLabel)
    move_player_signal = pyqtSignal(QLabel, int)
    move_enemy_signal = pyqtSignal(int, int)

    def __init__(self, enemy_list, print_modifier, gameplay, parent=None):
        QThread.__init__(self, parent)
        self.enemies = enemy_list
        self.printer = print_modifier
        self.gameplay = gameplay

    def run(self):
        self.move_enemies(enemy_list=self.enemies)

    def move_enemies(self, enemy_list):
        direction = "left"
        while True:
            if direction == "left":
                for i in range(30):
                    self.move_enemy_signal.emit(i, enemy_list[i].x() - 10)
                if enemy_list[0].x() <= 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    self.move_enemy_signal.emit(i, enemy_list[i].x() + 10)
                if enemy_list[-1].x() >= 740:
                    direction = "left"
            time.sleep(self.gameplay.enemy_speed)

    @pyqtSlot(int, int)
    def move_player(self, key, playerId):

        avatar = self.printer.label_avatar[playerId]

        if key == Qt.Key_Left:
            if avatar.x() > 10:
                self.move_player_signal.emit(avatar, avatar.x() - 10)

        elif key == Qt.Key_Right:
            if avatar.x() < 740:
                self.move_player_signal.emit(avatar, avatar.x() + 10)

        elif key == Qt.Key_Up:
            self.create_projectile_signal.emit(avatar)

