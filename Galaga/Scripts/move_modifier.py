from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading


class MoveModifer(QThread):

    def __init__(self, enemy_list, print_modifier, projectile_modifier):
        super().__init__(parent=None)
        self.mutex = Lock()
        self.enemies = enemy_list
        self.printer = print_modifier
        self.projectiles = projectile_modifier

    def run(self):
        self.move_enemies(enemy_list=self.enemies)

    def move_enemies(self, enemy_list):
        direction = "left"
        while True:
            self.mutex.acquire()
            if direction == "left":
                for i in range(30):
                    enemy_list[i].move(enemy_list[i].x() - 10, enemy_list[i].y())
                if enemy_list[0].x() == 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    enemy_list[i].move(enemy_list[i].x() + 10, enemy_list[i].y())
                if enemy_list[29].x() == 740:
                    direction = "left"
            self.mutex.release()
            time.sleep(0.5)

    def move_player(self, key):
        self.mutex.acquire()
        avatar1 = self.printer.label_avatar1
        avatar2 = self.printer.label_avatar2

        if key == Qt.Key_Left:
            if avatar1.x() > 10:
                avatar1.move(avatar1.x() - 10, avatar1.y())

        elif key == Qt.Key_Right:
            if avatar1.x() < 740:
                avatar1.move(avatar1.x() + 10, avatar1.y())

        elif key == Qt.Key_A:
            if avatar2.x() > 10:
                avatar2.move(avatar2.x() - 10, avatar2.y())

        elif key == Qt.Key_D:
            if avatar2.x() < 740:
                avatar2.move(avatar2.x() + 10, avatar2.y())

        elif key == Qt.Key_Up:
            self.projectiles.print_projectile(avatar1)

        elif key == Qt.Key_W:
            self.projectiles.print_projectile(avatar2)

        self.mutex.release()
