from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel
import time
from Galaga.Scripts.my_thread import MyThread
from Galaga.Sockets.socket_send import *


class MoveModifer(QThread):

    create_projectile_signal = pyqtSignal(QLabel)
    move_player_signal = pyqtSignal(QLabel, int)
    move_enemy_signal = pyqtSignal(int, int)
    good_power_signal = pyqtSignal()
    bad_power_signal = pyqtSignal(int)
    gift_remove_signal = pyqtSignal()

    def __init__(self, enemy_list, print_modifier, gameplay, gifts, parent=None):
        QThread.__init__(self, parent)
        self.enemies = enemy_list
        self.printer = print_modifier
        self.gameplay = gameplay
        self.gifts = gifts
        self.gift_type = True
        self.can_enemy_move = True

    def run(self):
        self.move_enemies(enemy_list=self.enemies)

    def move_enemies(self, enemy_list):
        direction = "left"
        while True:
            if self.can_enemy_move:
                if direction == "left":
                    for i in range(30):
                        self.move_enemy_signal.emit(i, enemy_list[i].x() - 10)
                    if enemy_list[-1].x() <= 10:
                        direction = "right"
                elif direction == "right":
                    for i in range(30):
                        self.move_enemy_signal.emit(i, enemy_list[i].x() + 10)
                    if enemy_list[0].x() >= 740:
                        direction = "left"
            time.sleep(self.gameplay.enemy_speed)


    @pyqtSlot(int)
    def move_player(self, key):

        avatar1 = self.printer.label_avatar1
        avatar2 = self.printer.label_avatar2
        if key == Qt.Key_Left:
            if avatar1.x() > 10:
                self.move_player_signal.emit(avatar1, avatar1.x() - 10)
                self.check_collision(avatar1)

        elif key == Qt.Key_Right:
            if avatar1.x() < 740:
                self.move_player_signal.emit(avatar1, avatar1.x() + 10)
                self.check_collision(avatar1)

        elif key == Qt.Key_A:
            if avatar2.x() > 10:
                self.move_player_signal.emit(avatar2, avatar2.x() - 10)
                self.check_collision(avatar2)

        elif key == Qt.Key_D:
            if avatar2.x() < 740:
                self.move_player_signal.emit(avatar2, avatar2.x() + 10)
                self.check_collision(avatar2)

        elif key == Qt.Key_Up:
            self.create_projectile_signal.emit(avatar1)

        elif key == Qt.Key_W:
            self.create_projectile_signal.emit(avatar2)

    def check_collision(self, avatar):
        for gift in self.gifts:
            if gift.isVisible():
                if gift.x() <= avatar.x() <= gift.x() + 40:
                    if self.gift_type:
                        self.good_power_signal.emit()
                        self.gift_remove_signal.emit()
                        self.gifts.remove(gift)
                    else:
                        self.bad_power_signal.emit(avatar.index)
                        self.gift_remove_signal.emit()
                        self.gifts.remove(gift)

    @pyqtSlot()
    def change_enemies_movement(self):
        self.can_enemy_move = not self.can_enemy_move

    @pyqtSlot(bool)
    def change_gift_type(self, gift):
        self.gift_type = gift

class GiftPower(QThread):

    change_movement_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.good_power = False

    def run(self):
        self.check_power()

    def check_power(self):
        while True:
            if self.good_power:
                self.change_movement_signal.emit()
                time.sleep(4)
                self.change_movement_signal.emit()
                self.good_power = False

            time.sleep(0.5)

    @pyqtSlot()
    def work(self):
        self.good_power = True