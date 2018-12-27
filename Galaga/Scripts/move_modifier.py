from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading


class MoveModifer(QThread):

    def __init__(self, enemy_list):
        super().__init__(parent=None)
        self.mutex = Lock()
        self.enemies = enemy_list

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

    def move_player(self, player1, player2, key):
        self.mutex.acquire()
        avatar1 = player1
        avatar2 = player2

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
            Gameplay.create_projectile(self, avatar1)

        elif key == Qt.Key_W:
            Gameplay.create_projectile(self, avatar2)

        self.mutex.release()

    def move_projectiles(self, projectile_list):
        while True:
            self.mutex.acquire()
            if len(self.projectile_list) > 0:
                for i in range(len(self.projectile_list)):
                    if self.projectile_list[i].y() <= 0:
                        self.projectile_list[i].hide()
                    else:
                        self.projectile_list[i].move(self.projectile_list[i].x(), self.projectile_list[i].y() - 20)
                self.mutex.release()
                time.sleep(0.1)
