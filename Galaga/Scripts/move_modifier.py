from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading
from Galaga.Scripts.my_thread import MyThread


class MoveModifer(MyThread):

    create_projectile = pyqtSignal(QLabel)


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
                    self.mutex.acquire()
                    enemy_list[i].move(enemy_list[i].x() - 10, enemy_list[i].y())
                    self.mutex.release()
                if enemy_list[0].x() == 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    self.mutex.acquire()
                    enemy_list[i].move(enemy_list[i].x() + 10, enemy_list[i].y())
                    self.mutex.release()
                if enemy_list[29].x() == 740:
                    direction = "left"
            time.sleep(0.5)

    def move_player(self, key):

        avatar1 = self.printer.label_avatar1
        avatar2 = self.printer.label_avatar2

        if key == Qt.Key_Left:
            if avatar1.x() > 10:
                self.mutex.acquire()
                avatar1.move(avatar1.x() - 10, avatar1.y())
                self.mutex.release()

        elif key == Qt.Key_Right:
            if avatar1.x() < 740:
                self.mutex.acquire()
                avatar1.move(avatar1.x() + 10, avatar1.y())
                self.mutex.release()

        elif key == Qt.Key_A:
            if avatar2.x() > 10:
                self.mutex.acquire()
                avatar2.move(avatar2.x() - 10, avatar2.y())
                self.mutex.release()

        elif key == Qt.Key_D:
            if avatar2.x() < 740:
                self.mutex.acquire()
                avatar2.move(avatar2.x() + 10, avatar2.y())
                self.mutex.release()

        elif key == Qt.Key_Up:
            self.create_projectile.emit(avatar1)

        elif key == Qt.Key_W:
            self.create_projectile.emit(avatar2)

