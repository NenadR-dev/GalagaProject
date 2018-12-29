from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel
from Galaga.Scripts.my_thread import MyThread
import time


class ProjectileModifier(MyThread):

    projectile_move_signal = pyqtSignal(QLabel, int)
    projectile_remove_signal = pyqtSignal(QLabel)

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
                        self.projectile_remove_signal.emit(projectile)
                        projectile_list.remove(projectile)
                        self.mutex.release()
                    else:
                        self.projectile_move_signal.emit(projectile, projectile.y() - 5)
                        self.check_collision(projectile_list, projectile)

            time.sleep(0.02)

    def check_collision(self, projectile_list, projectile):
        if projectile.isVisible() and projectile.y() <= 160:
            for enemy in reversed(self.enemies):
                if enemy.isVisible() and projectile.y() <= enemy.y():
                    if enemy.x() <= projectile.x() <= enemy.x() + 50:
                        self.mutex.acquire()
                        projectile.hide()
                        projectile_list.remove(projectile)
                        enemy.hide()
                        self.projectile_remove_signal.emit(projectile)
                        self.gameplay.count_killed_enemies()
                        self.mutex.release()
                        break

    @pyqtSlot(QLabel)
    def add_projectile(self, projectile):
        self.projectile_mutex.acquire()
        self.projectiles.append(projectile)
        self.projectile_mutex.release()

class EnemyProjectileModifier(MyThread):

    projectile_move_signal = pyqtSignal(QLabel, int)

    def __init__(self, avatar1, avatar2, print_modifier, gameplay):
        super().__init__(parent=None)
        self.enemies = [avatar1, avatar2]
        self.printer = print_modifier
        self.projectiles = []
        self.gameplay = gameplay

    def run(self):
        self.move_projectiles(projectile_list=self.projectiles)

    def move_projectiles(self, projectile_list):
        while True:
            if len(projectile_list) > 0:
                for projectile in projectile_list:
                    if projectile.y() >= 600:
                        self.mutex.acquire()
                        projectile.hide()
                        # ^  mozda bi ipak trebalo sa ostalim iscrtavanjem
                        # |  ali ovde radi + ne puca
                        projectile_list.remove(projectile)
                        self.mutex.release()
                    else:
                        self.projectile_move_signal.emit(projectile, projectile.y() + 5)
                        self.check_collision(projectile_list, projectile)

            time.sleep(0.02)

    def check_collision(self, projectile_list, projectile):
        if projectile.isVisible() and projectile.y() >= 540:
            index = len(self.enemies) + 1
            for enemy in reversed(self.enemies):
                index -= 1
                if enemy.isVisible() and projectile.y() >= enemy.y():
                    if enemy.x() <= projectile.x() <= enemy.x() + 50:
                        self.mutex.acquire()
                        projectile.hide()
                        projectile_list.remove(projectile)
                        self.gameplay.player_hit(index)
                        self.mutex.release()
                        break

    @pyqtSlot(QLabel)
    def add_projectile(self, projectile):
        self.projectile_mutex.acquire()
        self.projectiles.append(projectile)
        self.projectile_mutex.release()
