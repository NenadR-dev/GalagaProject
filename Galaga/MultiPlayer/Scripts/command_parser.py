from Galaga.MultiPlayer.Common.common_thread import CommonThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread

class CommandParser(QThread):

    move_player_signal = pyqtSignal(int, int)
    fire_projectile_signal = pyqtSignal(int)
    start_game_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str)
    def parse_command(self, param, command):
        CommonThread.mutex_movement.acquire()
        if command == 'move_up':
            self.fire_projectile_signal.emit(Qt.Key_Up, param)
        elif command == 'move_left':
            self.move_player_signal.emit(Qt.Key_Left, param)
        elif command == 'move_right':
            self.move_player_signal.emit(Qt.Key_Right, param)
        elif command == 'start_game':
            self.start_game_signal.emit(param)
        CommonThread.mutex_movement.release()
