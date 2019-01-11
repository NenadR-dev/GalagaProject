from PyQt5.QtCore import pyqtSignal, QThread
import time, random
from Galaga.Scripts.my_thread import MyThread


class EnemyMoveAttack(QThread):

    enemy_attack_move_signal = pyqtSignal(int, int, int)
    return_enemy_signal = pyqtSignal(int, bool)
    player_hit_signal = pyqtSignal(int)

    def __init__(self, enemy_list, avatar_list, gameplay, parent=None):
        QThread.__init__(self, parent)
        self.enemies = enemy_list
        self.avatars = avatar_list
        self.gameplay = gameplay
        self.can_move = False

    def run(self):
        self.enemy_clock()

    def kill_avatar_success(self, avatar_index, enemy_index):
        self.player_hit_signal.emit(avatar_index)
        self.return_enemy_signal.emit(enemy_index, True)

    def kill_avatar_fail(self, enemy_index):
        self.return_enemy_signal.emit(enemy_index, False)

    def start_enemy_attack(self):
        enemy_index = random.randint(0, len(self.enemies) - 1)
        avatar_index = random.randint(0, len(self.avatars))
        while not self.avatars[avatar_index].isVisible():
            avatar_index = random.randint(len(self.avatars))
        avatar = self.avatars[avatar_index]
        enemy = self.enemies[enemy_index]
        x_coord_diff = enemy.x() - avatar.x()
        self.movement_factor = 0
        while enemy.y() < 540:
            if x_coord_diff > 0:
                self.movement_factor = random.randint(-20, 10)
            elif x_coord_diff < 0:
                self.movement_factor = random.randint(-10, 20)
            else:
                self.movement_factor = random.randint(-15, 15)
            self.enemy_attack_move_signal.emit(enemy_index, self.movement_factor, 5)
            x_coord_diff += self.movement_factor
            time.sleep(0.02)
        success = False
        for avatar in self.avatars:
            if avatar.isVisible() and abs(enemy.x() - avatar.x()) <= 50:
                self.kill_avatar_success(avatar.index, enemy_index)
                success = True
        if not success:
            self.kill_avatar_fail(enemy_index)

    def enemy_clock(self):
        time.sleep(5)
        while True:
            time_delay = random.randrange(5, 10)
            time.sleep(time_delay)
            if any(avatar.isVisible() for avatar in self.avatars):
                self.start_enemy_attack()


class EnemyProjectileAttack(QThread):

    enemy_attack_projectile_signal = pyqtSignal(int)

    def __init__(self, enemy_list, avatar_list):
        super().__init__(parent=None)
        self.enemies = enemy_list
        self.avatars = avatar_list

    def run(self):
        self.enemy_clock()

    def start_enemy_attack(self):
        enemy_index = random.randint(0, len(self.enemies) - 1)
        if self.enemies[enemy_index].isVisible():
            self.enemy_attack_projectile_signal.emit(enemy_index)

    def enemy_clock(self):
        time.sleep(1)
        while True:
            time_delay = random.randrange(1, 2)
            time.sleep(time_delay)
            if any(avatar.isVisible() for avatar in self.avatars):
                self.start_enemy_attack()
