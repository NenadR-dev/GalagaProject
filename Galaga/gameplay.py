from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from Galaga.Scripts.my_thread import MyThread


class Gameplay(QThread):

    next_level_signal = pyqtSignal()
    player_killed_signal = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self, parent=None)
        self.enemy_speed = 0.5
        self.enemies_killed = 0
        self.avatar1_lifes = 3
        self.avatar2_lifes = 3
        self.level = 1

    def run(self):
        pass

    @pyqtSlot()
    def count_killed_enemies(self):
        MyThread.gameplay_lock.acquire()
        self.enemies_killed += 1
        print("enemies killed => {}".format(self.enemies_killed))
        MyThread.gameplay_lock.release()
        if self.enemies_killed == 30:
            self.new_level()

    @pyqtSlot(int)
    def player_hit(self, avatar):
        if avatar == 1:
            if self.avatar1_lifes > 1:  # ako ima 1 smanjuje mu se na 0 i odmah je mrtav
                MyThread.gameplay_lock.acquire()
                self.avatar1_lifes -= 1
                print('player1 lifes: {}'.format(self.avatar1_lifes))
                MyThread.gameplay_lock.release()
            else:
                MyThread.gameplay_lock.acquire()
                self.avatar1_lifes -= 1
                self.player_killed_signal.emit(1)
                MyThread.gameplay_lock.release()
        elif avatar == 2:
            if self.avatar2_lifes > 1:
                MyThread.gameplay_lock.acquire()
                self.avatar2_lifes -= 1
                print('player2 lifes: {}'.format(self.avatar2_lifes))
                MyThread.gameplay_lock.release()
            else:
                MyThread.gameplay_lock.acquire()
                self.avatar2_lifes -= 1
                self.player_killed_signal.emit(2)
                MyThread.gameplay_lock.release()

    def new_level(self):
        if self.enemy_speed > 0.06:
            MyThread.gameplay_lock.acquire()
            self.enemy_speed -= 0.05
            self.level += 1
            print('level:{} speed => {}'.format(self.level, self.enemy_speed))
            self.enemies_killed = 0
            if self.avatar1_lifes > 0:
                self.avatar1_lifes = 3
            else:
                pass  # UMRO JE I NE TREBA GA VRACATI

            if self.avatar2_lifes > 0:
                self.avatar2_lifes = 3
            else:
                pass  # UMRO JE I NE TREBA GA VRACATI

            self.next_level_signal.emit()
            MyThread.gameplay_lock.release()
        else:
            MyThread.gameplay_lock.acquire()
            self.enemy_speed = 0.05
            self.level += 1
            print('level:{} speed => {}'.format(self.level, self.enemy_speed))
            self.enemies_killed = 0
            if self.avatar1_lifes > 0:
                self.avatar1_lifes = 3
            else:
                pass  # UMRO JE I NE TREBA GA VRACATI

            if self.avatar2_lifes > 0:
                self.avatar2_lifes = 3
            else:
                pass  # UMRO JE I NE TREBA GA VRACATI

            self.next_level_signal.emit()
            MyThread.gameplay_lock.release()
