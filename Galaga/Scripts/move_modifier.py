from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading
from Galaga.Scripts.my_thread import MyThread


class MoveModifer(MyThread):

    create_projectile_signal = pyqtSignal(QLabel)
    move_player_signal = pyqtSignal(int, int)
    move_enemy_signal = pyqtSignal(int, int)

    def __init__(self, enemy_list, print_modifier):
        super().__init__(parent=None)
        self.enemies = enemy_list
        self.printer = print_modifier

    def run(self):
        self.move_enemies(enemy_list=self.enemies)

    def move_enemies(self, enemy_list):
        direction = "left"
        while True:
            if direction == "left":
                for i in range(30):
                    self.move_enemy_signal.emit(i, enemy_list[i].x() - 10)
                if enemy_list[0].x() == 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    self.move_enemy_signal.emit(i, enemy_list[i].x() + 10)
                if enemy_list[29].x() == 740:
                    direction = "left"
            time.sleep(0.5)

    def move_player(self, key):

        avatar1 = self.printer.label_avatar1
        avatar2 = self.printer.label_avatar2

        if key == Qt.Key_Left:
            if avatar1.x() > 10:
                self.move_player_signal.emit(1, avatar1.x() - 10)

        elif key == Qt.Key_Right:
            if avatar1.x() < 740:
                self.move_player_signal.emit(1, avatar1.x() + 10)

        elif key == Qt.Key_A:
            if avatar2.x() > 10:
                self.move_player_signal.emit(2, avatar2.x() - 10)

        elif key == Qt.Key_D:
            if avatar2.x() < 740:
                self.move_player_signal.emit(2, avatar2.x() + 10)

        elif key == Qt.Key_Up:
            self.create_projectile_signal.emit(avatar1)

        elif key == Qt.Key_W:
            self.create_projectile_signal.emit(avatar2)

