from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QLabel
from Galaga.Scripts.my_thread import MyThread
import time


class ProjectileModifier(QThread):

    projectile_move_signal = pyqtSignal(QLabel, int)

    def __init__(self, projectile_list, parent=None):
        QThread.__init__(self, parent)
        self.projectiles = projectile_list

    def run(self):
        self.move_projectiles(projectile_list=self.projectiles)

    def move_projectiles(self, projectile_list):
        while True:
            if len(projectile_list) > 0:
                for projectile in projectile_list:
                    self.projectile_move_signal.emit(projectile, projectile.y() - 5)
            time.sleep(0.02)
