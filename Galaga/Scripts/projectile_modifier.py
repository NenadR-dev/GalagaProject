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
            print(len(projectile_list))
            self.projectile_mutex.acquire
            if len(projectile_list) > 0:
                for projectile in projectile_list:
                    if projectile.y() <= 0:
                        self.mutex.acquire()
                        projectile_list.remove(projectile)
                        self.mutex.release()
                    else:
                        self.mutex.acquire()
                        projectile.move(projectile.x(), projectile.y() - 20)
                        self.mutex.release()
                        self.check_collision(projectile_list, projectile)
            self.projectile_mutex.release

            time.sleep(0.1)

    def check_collision(self, projectile_list, projectile):
        if projectile.isVisible() and projectile.y() < 160:
            for enemy in reversed(self.enemies):
                if enemy.isVisible() and projectile.y() <= enemy.y():
                    if enemy.x() + 50 >= projectile.x() and enemy.x() <= projectile.x():
                        self.mutex.acquire()
                        projectile.hide()
                        projectile_list.remove(projectile)
                        enemy.hide()
                        self.mutex.release()
                        break

    @pyqtSlot(QLabel)
    def add_projectile(self, projectile):
        self.projectile_mutex.acquire
        self.projectiles.append(projectile)
        self.projectile_mutex.release