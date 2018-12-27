from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading


class ProjectileModifier(QThread):

    def __init__(self, enemy_list, print_modifier):
        super().__init__(parent=None)
        self.mutex = Lock()
        self.enemies = enemy_list
        self.printer = print_modifier
        self.projectiles = []

    def run(self):
        self.move_projectiles(projectile_list=self.projectiles)

    def print_projectile(self, avatar):
        self.mutex.acquire()
        self.printer.print_projectile(avatar, self.projectiles)
        self.mutex.release()

    def move_projectiles(self, projectile_list):
        while True:
            self.mutex.acquire()
            if len(projectile_list) > 0:
                for i in range(len(projectile_list)):
                    if projectile_list[i].y() <= 0:
                        projectile_list[i].hide()
                    else:
                        projectile_list[i].move(projectile_list[i].x(), projectile_list[i].y() - 20)
                        self.check_collision(projectile_list[i])
            self.mutex.release()
            time.sleep(0.1)

    def check_collision(self, projectile):
        if projectile.isVisible() and projectile.y() < 160:
            for enemy in reversed(self.enemies):
                if enemy.isVisible() and projectile.y() <= enemy.y():
                    if enemy.x() + 50 >= projectile.x() and enemy.x() <= projectile.x():
                        projectile.hide()
                        enemy.hide()
                        break