from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel
import time
from Galaga.Scripts.my_thread import MyThread
from Galaga.Sockets.socket_send import *


class ServerMoveModifier(QThread):

    create_projectile_signal = pyqtSignal(int)
    move_player_signal = pyqtSignal(QLabel, int)
    move_enemy_signal = pyqtSignal(int, int)

    def __init__(self, enemy_list, print_modifier, server, gameplay, parent=None):
        QThread.__init__(self, parent)
        self.enemies = enemy_list
        self.printer = print_modifier
        self.gameplay = gameplay
        self.server_modifier = server

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
            command = 'command-{}-move_enemy'.format(direction)
            print(command)
            self.server_modifier.send_command(command)
            time.sleep(self.gameplay.enemy_speed)

    @pyqtSlot(str)
    def move_player(self, params):
        param = params.split(':')
        key = int(param[1])
        playerId = int(param[0])
        print('moving player: {}'.format(playerId))
        avatar = self.printer.label_avatar[playerId]
        if key == Qt.Key_Left:
            if avatar.x() > 10:
                self.move_player_signal.emit(avatar, avatar.x() - 10)
                command = 'command-{}:{}-move_player'.format(playerId, avatar.x())
                self.server_modifier.send_command(command)
        elif key == Qt.Key_Right:
            if avatar.x() < 740:
                self.move_player_signal.emit(avatar, avatar.x() + 10)
                command = 'command-{}:{}-move_player'.format(playerId, avatar.x())
                self.server_modifier.send_command(command)
        elif key == Qt.Key_Up:
            self.create_projectile_signal.emit(playerId)
            command = 'command-{}-print_projectile'.format(playerId)
            self.server_modifier.send_command(command)
