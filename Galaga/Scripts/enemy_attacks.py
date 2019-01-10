from PyQt5.QtCore import pyqtSignal, QThread
import time, random
from multiprocessing import Queue
from Galaga.Scripts.my_thread import MyThread
from Galaga.Scripts.my_process import MyProcess


class EnemyMoveAttack(QThread):

    enemy_attack_move_signal = pyqtSignal(int, int, int)
    return_enemy_signal = pyqtSignal(int, bool)
    player_hit_singal = pyqtSignal(int)

    def __init__(self, enemy_list, avatar1, avatar2, gameplay, parent=None):
        QThread.__init__(self, parent)
        self.enemies = enemy_list
        self.avatar1 = avatar1
        self.avatar2 = avatar2
        self.gameplay = gameplay
        self.can_move = True
        self.queue = Queue()
        self.process = MyProcess(enemy_list, self.queue)

    def run(self):
        self.enemy_clock()

    def kill_avatar_success(self, avatar_index, enemy_index):
        self.player_hit_singal.emit(avatar_index)
        self.return_enemy_signal.emit(enemy_index, True)

    def kill_avatar_fail(self, enemy_index):
        self.return_enemy_signal.emit(enemy_index, False)

    def start_enemy_attack(self):
        #enemy_index = random.randint(0, len(self.enemies) - 1)
        #self.process.process()
        enemy_index = self.queue.get()  # process

        avatar = self.avatar1
        if self.avatar1.isVisible():
            avatar = self.avatar1
            if self.avatar2.isVisible():
                if random.randint(1, 2) == 2:
                    avatar = self.avatar2
        elif self.avatar2.isVisible():
            avatar = self.avatar2
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
        if self.avatar1.isVisible() and abs(enemy.x() - self.avatar1.x()) <= 50:
            self.kill_avatar_success(1, enemy_index)
        elif self.avatar1.isVisible() and abs(enemy.x() - self.avatar2.x()) <= 50:
            self.kill_avatar_success(2, enemy_index)
        else:
            self.kill_avatar_fail(enemy_index)

    def enemy_clock(self):
        time.sleep(5)
        while True:
            time_delay = random.randrange(5, 10)
            time.sleep(time_delay)
            if self.avatar1.isVisible() or self.avatar2.isVisible():
                self.start_enemy_attack()


class EnemyProjectileAttack(QThread):

    enemy_attack_projectile_signal = pyqtSignal(int)

    def __init__(self, enemy_list, avatar1, avatar2):
        super().__init__(parent=None)
        self.enemies = enemy_list
        self.avatar1 = avatar1
        self.avatar2 = avatar2

    def run(self):
        self.enemy_clock()

    def start_enemy_attack(self):
        enemy_index = random.randint(0, len(self.enemies) - 1)
        self.enemy_attack_projectile_signal.emit(enemy_index)

    def enemy_clock(self):
        time.sleep(1)
        while True:
            time_delay = random.randrange(1, 2)
            time.sleep(time_delay)
            if self.avatar1.isVisible() or self.avatar2.isVisible():
                self.start_enemy_attack()
