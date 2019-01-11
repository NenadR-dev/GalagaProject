from Galaga.MultiPlayer.Common.common_thread import CommonThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread


class CommandParser(QThread):

    move_player_signal = pyqtSignal(str)
    fire_projectile_signal = pyqtSignal(int)
    start_game_signal = pyqtSignal(str)
    move_enemy_signal = pyqtSignal(str)
    move_projectile_signal = pyqtSignal(str)
    remove_projectile_signal = pyqtSignal(int)
    remove_enemy_signal = pyqtSignal(int)
    next_level_signal = pyqtSignal()
    enemy_projectile_attack_signal = pyqtSignal(int)
    enemy_kamikaze_signal = pyqtSignal(int)
    remove_player_signal = pyqtSignal(int)
    print_player_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str)
    def parse_command(self, param, command):
        CommonThread.mutex_movement.acquire()
        if command == 'create_projectile':
            print('player {} fired a bullet'.format(param))
            self.fire_projectile_signal.emit(int(param)) #param se salje kao index
        elif command == 'move_player':
            print('{} -> {}'.format(command, param))
            self.move_player_signal.emit(param)  #param se salje kao id:key
        elif command == 'print_player':
            print(command + param)
            self.print_player_signal.emit(param) #salje se kao index:position
        elif command == 'start_game':
            print('player count: {} avatar id: {}'.format(command, param))
            self.start_game_signal.emit(param)  #param se salje kao player_count:player_id
        elif command == 'move_enemy':
            self.move_enemy_signal.emit(param)  #param se salje kao index:position
        elif command == 'move_projectile':
            self.move_projectile_signal.emit(param) #param se salje kao index:position
        elif command == 'remove_projectile':
            print(command)
            self.remove_projectile_signal.emit(int(param))
        elif command == 'remove_enemy':
            print(command)
            self.remove_enemy_signal.emit(int(param))
        elif command == 'next_level':
            print(command)
            self.next_level_signal.emit()
        elif command == 'enemy_projectile_attack':
            print(command)
            self.enemy_projectile_attack_signal.emit(int(param))
        elif command == 'enemy_kamikaze':
            print(command)
            self.enemy_kamikaze_signal.emit(param)  #param se salje kao index:x-osa:y-osa
        elif command == 'remove_player':
            print(command)
            self.remove_player_signal.emit(int(param))
        CommonThread.mutex_movement.release()
