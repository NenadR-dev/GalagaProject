from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading
from Galaga.Scripts.print_modifier import PrintModifier, MoveModifer


class Gameplay(QWidget, QObject):

    finished = pyqtSignal()
    projectile_list = []
    mutex = Lock()

    @pyqtSlot()
    def enemies_movement(self):
        direction = "left"
        while True:
            if direction == "left":
                for i in range(30):
                    self.list[i].move(self.list[i].x() - 10, self.list[i].y())
                if self.list[0].x() == 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    self.list[i].move(self.list[i].x() + 10, self.list[i].y())
                if self.list[29].x() == 740:
                    direction = "left"
            time.sleep(0.3)

    def move_projectile(self):
        while True:
            if len(self.projectile_list) > 0:
                for i in range(len(self.projectile_list)):
                    if self.projectile_list[i].y() <= 0:
                        self.projectile_list[i].hide()
                    else:
                        self.projectile_list[i].move(self.projectile_list[i].x(), self.projectile_list[i].y() - 20)
                time.sleep(0.1)

    def __update_position__(self, key):
        self.movement.move_player(self.print.label_avatar1, self.print.label_avatar2, key)