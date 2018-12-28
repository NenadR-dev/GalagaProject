from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
from Galaga.Scripts.my_thread import MyThread
import time, threading


class ProjectileModifier(MyThread):


    def __init__(self, enemy_list, print_modifier):
        super().__init__(parent=None)
        self.enemies = enemy_list
        self.printer = print_modifier
        self.projectiles = []

    def run(self):
        self.move_projectiles(projectile_list=self.projectiles)

    def move_projectiles(self, projectile_list):
        while True:
            if len(projectile_list) > 0:
                for i in projectile_list:
                    if i.y() <= 0:
                        self.mutex.acquire()
                        i.hide()
                        self.mutex.release()
                    else:
                        self.mutex.acquire()
                        i.move(i.x(), i.y() - 20)
                        self.check_collision(i)

            time.sleep(0.1)

    def check_collision(self, projectile):
        if projectile.isVisible() and projectile.y() < 160:
            for enemy in reversed(self.enemies):
                if enemy.isVisible() and projectile.y() <= enemy.y():
                    if enemy.x() + 50 >= projectile.x() and enemy.x() <= projectile.x():
                        self.mutex.acquire()
                        projectile.hide()
                        enemy.hide()
                        self.mutex.release()
                        break

    @pyqtSlot(QLabel)
    def add_projectile(self, projectile):
        self.projectiles.append(projectile)