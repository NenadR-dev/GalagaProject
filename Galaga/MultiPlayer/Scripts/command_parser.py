from Galaga.MultiPlayer.Common.common_thread import CommonThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class CommandParser(CommonThread):

    move_player_signal = pyqtSignal(int, int)
    fire_projectile_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str)
    def parse_command(self, player_id, command):
        CommonThread.mutex_movement.acquire()
        if command == 'move_up':
            self.fire_projectile_signal.emit(player_id)
        elif command == 'move_left':
            self.move_player_signal.emit(player_id, -5)
        elif command == 'move_right':
            self.move_player_signal.emit(player_id, +5)
        CommonThread.mutex_movement.release()