from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
import time, threading, random

def kill_enemy(self, enemy):
    print("killed")
    enemy.hide()


def kill_avatar_success(self, avatar, enemy):
    print("killed")
    avatar.hide()
    self.self.kill_enemy(enemy)


def kill_avatar_fail(self, enemy):
    print("failed")


def start_enemy_attack(self):
    enemy = self.list[random.randint(0, 29)]
    avatar = self.label_avatar1
    if random.randint(1, 2) == 2:
        avatar = self.label_avatar2
    avatar_coord_x = avatar.x()
    x_coord_diff = enemy.x() - avatar_coord_x
    while enemy.y() > 60:
        if x_coord_diff > 0:
            enemy.move(enemy.x() - 1, enemy.y() - 1)
            x_coord_diff -= 1
        elif x_coord_diff > 0:
            enemy.move(enemy.x() + 1, enemy.y() - 1)
            x_coord_diff += 1
        else:
            enemy.move(enemy.x(), enemy.y() - 1)
    if abs(enemy.x() - avatar.x()) <= 50:
        self.kill_avatar_success(avatar, enemy)
    else:
        self.kill_avatar_fail(enemy)


@pyqtSlot()
def enemy_clock(self):
    time.sleep(10)
    while True:
        timeDelay = random.randrange(5, 10)
        time.sleep(timeDelay)
        self.start_enemy_attack()
