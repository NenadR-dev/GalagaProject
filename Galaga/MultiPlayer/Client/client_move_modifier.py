from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel
from Galaga.Sockets.socket_send import *


class ClientMultiplayerMoveModifer(QThread):

    create_projectile_signal = pyqtSignal(QLabel)
    move_player_signal = pyqtSignal(QLabel, int)
    move_enemy_signal = pyqtSignal(int, int)
    move_projectile_signal = pyqtSignal(int, int)

    def __init__(self, print_modifier,  parent=None):
        QThread.__init__(self, parent)
        self.printer = print_modifier

    def run(self):
        self.move_enemies(enemy_list=self.enemies)

    @pyqtSlot(str)
    def move_enemy(self, new_position):
        params = new_position.split(':')
        self.move_enemy_signal.emit(int(params[0]), int(params[1]))

    @pyqtSlot(str)
    def move_projectile(self, param):
        position = param.split(':')
        self.move_projectile_signal.emit(int(param[0]), int(param[1]))

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

