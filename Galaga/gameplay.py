from PyQt5.QtCore import pyqtSignal
from Galaga.Scripts.my_thread import MyThread


class Gameplay(MyThread):

    next_level_signal = pyqtSignal()
    player_killed_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.enemy_speed = 0.5
        self.enemies_killed = 0
        self.avatar1_lifes = 3
        self.avatar2_lifes = 3

    def run(self):
        print()

    def count_killed_enemies(self):
        self.enemies_killed += 1
        if self.enemies_killed == 30:
            self.new_level()

    def player_hit(self, avatar):
        if avatar == 1:
            if self.avatar1_lifes > 0:
                self.avatar1_lifes -= 1
            else:
                self.player_killed_signal.emit(1)
        elif avatar == 2:
            if self.avatar2_lifes > 0:
                self.avatar2_lifes -= 1
            else:
                self.player_killed_signal.emit(2)

    def new_level(self):
        if self.enemy_speed > 0:
            self.enemy_speed -= 0.025
            self.enemies_killed = 0
            if self.avatar1_lifes > 0:
                self.avatar1_lifes = 3
            else:
                print()  # UMRO JE I NE TREBA GA VRACATI

            if self.avatar2_lifes > 0:
                self.avatar2_lifes = 3
            else:
                print()  # UMRO JE I NE TREBA GA VRACATI

            self.next_level_signal.emit()
        else:
            self.enemy_speed = 0
            self.enemies_killed = 0
            if self.avatar1_lifes > 0:
                self.avatar1_lifes = 3
            else:
                print()  # UMRO JE I NE TREBA GA VRACATI

            if self.avatar2_lifes > 0:
                self.avatar2_lifes = 3
            else:
                print()  # UMRO JE I NE TREBA GA VRACATI

            self.next_level_signal.emit()