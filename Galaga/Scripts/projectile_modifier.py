from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
from Galaga.Scripts.my_thread import MyThread
import time, threading


class ProjectileModifier(MyThread):

    projectile_move_signal = pyqtSignal(QLabel, int)

    def __init__(self, enemy_list, print_modifier, gameplay):
        super().__init__(parent=None)
        self.enemies = enemy_list
        self.printer = print_modifier
        self.projectiles = []
        self.gameplay = gameplay

    def run(self):
        self.move_projectiles(projectile_list=self.projectiles)

    def move_projectiles(self, projectile_list):
        while True:
            if len(projectile_list) > 0:
                for projectile in projectile_list:
                    if projectile.y() <= 0:
                        self.mutex.acquire()
                        projectile.hide()
                        # ^  mozda bi ipak trebalo sa ostalim iscrtavanjem
                        # |  ali ovde radi + ne puca
                        projectile_list.remove(projectile)
                        self.mutex.release()
                    else:
                        self.projectile_move_signal.emit(projectile, projectile.y() - 5)
                        self.check_collision(projectile_list, projectile)

            time.sleep(0.025)

    def check_collision(self, projectile_list, projectile):
        if projectile.isVisible() and projectile.y() < 160:
            for enemy in reversed(self.enemies):
                if enemy.isVisible() and projectile.y() <= enemy.y():
                    if enemy.x() + 50 >= projectile.x() and enemy.x() <= projectile.x():
                        self.mutex.acquire()
                        projectile.hide()
                        projectile_list.remove(projectile)
                        enemy.hide()
                        self.gameplay.count_killed_enemies()
                        self.mutex.release()
                        break

    @pyqtSlot(QLabel)
    def add_projectile(self, projectile):
        self.projectile_mutex.acquire()
        self.projectiles.append(projectile)
        self.projectile_mutex.release()