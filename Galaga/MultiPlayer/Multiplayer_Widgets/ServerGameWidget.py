from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QWidget
from Galaga.MultiPlayer.Scripts.command_parser import CommandParser
from Galaga.MultiPlayer.Server.server_modifier import ServerModifer
from Galaga.MultiPlayer.Server.server_enemy_attacks import EnemyMoveAttack, EnemyProjectileAttack
from Galaga.MultiPlayer.Server.server_print_modifier import ServerPrintModifier
from Galaga.MultiPlayer.Server.server_projectile_modifier import ProjectileModifier, EnemyProjectileModifier
from Galaga.MultiPlayer.Server.server_move_modifier import ServerMoveModifier
from Galaga.Scripts.key_notifier import KeyNotifier
from Galaga.MultiPlayer.multiplayer_gameplay import Gameplay
from Galaga.MultiPlayer.Scripts.socket_monitor import SocketMonitor
from Galaga.MultiPlayer.Common.host_data import HostData


class ServerMainWindow(QWidget):

    move_player_signal = pyqtSignal(str)
    command_parser = CommandParser()
    server = ServerModifer()

    def __init__(self, parent=None):
        super(ServerMainWindow, self).__init__(parent)
        self.start_command_parser()
        self.server.daemon = True
        self.server.start()
        self.set_up_socket_connections()

    def set_up_socket_connections(self):
        for node in HostData.client_address:
            socket_monitor = SocketMonitor(HostData.client_address[node])
            socket_monitor.trigger_event_signal.connect(self.command_parser.parse_command)
            socket_monitor.daemon = True
            socket_monitor.start()

    def start_game(self, params):
        self.param = params.split(':')
        self.player_count = int(self.param[0])
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)

        self.start_ui_window(self.player_count)
        self.start_gameplay(self.player_count)
        self.start_key_notifier()

        #set gif animation
        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        #set avatars and projectile
        self.start_player_movement()
        #start projectile thread
        self.start_projectile_movement()
        #start enemy attacks
        #self.start_enemy_attacks()

    def start_enemy_attacks(self):
        self.enemy_move_attack = EnemyMoveAttack(self.Window.local_enemy_list, self.Window.label_avatar, self.gameplay)
        self.enemy_move_attack.enemy_attack_move_signal.connect(self.Window.enemy_move_attack)
        self.enemy_move_attack.return_enemy_signal.connect(self.Window.return_enemy)
        self.enemy_move_attack.player_hit_signal.connect(self.gameplay.player_hit)
        self.enemy_move_attack.daemon = True
        self.enemy_move_attack.start()

        self.enemy_projectile_attack = EnemyProjectileAttack(self.Window.local_enemy_list, self.Window.label_avatar)
        self.enemy_projectile_attack.enemy_attack_projectile_signal.connect(self.Window.enemy_projectile_attack)
        self.enemy_projectile_attack.daemon = True
        self.enemy_projectile_attack.start()


    def start_projectile_movement(self):
        self.projectiles = ProjectileModifier(self.Window.local_enemy_list, self.Window, self.gameplay)
        self.projectiles.enemy_killed_signal.connect(self.Window.remove_enemy)
        self.projectiles.projectile_move_signal.connect(self.Window.move_projectile)
        self.projectiles.projectile_remove_signal.connect(self.Window.remove_projectile)
        self.Window.move_p.connect(self.projectiles.add_projectile)
        self.Window.count_enemy_signal.connect(self.gameplay.count_killed_enemies)
        self.Window.remove_enemy_projectile_signal.connect(self.projectiles.remove_projectiles)
        self.command_parser.fire_projectile_signal.connect(self.Window.print_projectile)
        self.projectiles.daemon = True
        self.projectiles.start()

        self.enemy_projectiles = EnemyProjectileModifier(self.Window, self.gameplay)
        self.enemy_projectiles.projectile_move_signal.connect(self.Window.move_enemy_projectile)
        self.Window.move_enemy_p.connect(self.enemy_projectiles.add_projectile)
        self.enemy_projectiles.projectile_remove_signal.connect(self.projectiles.remove_projectiles)
        self.enemy_projectiles.player_hit_signal.connect(self.gameplay.player_hit)
        self.enemy_projectiles.daemon = True
        self.enemy_projectiles.start()


    def start_player_movement(self):
        self.player_movement = ServerMoveModifier(self.Window.local_enemy_list, self.Window ,self.server, self.gameplay)
        self.player_movement.create_projectile_signal.connect(self.Window.print_projectile)
        self.player_movement.move_enemy_signal.connect(self.Window.move_enemy)
        self.player_movement.move_player_signal.connect(self.Window.move_player)
        self.move_player_signal.connect(self.player_movement.move_player)
        self.command_parser.move_player_signal.connect(self.player_movement.move_player)
        self.player_movement.daemon = True
        self.player_movement.start()

    def start_key_notifier(self):
        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def start_gameplay(self, number_of_players):
        self.gameplay = Gameplay(number_of_players)
        self.gameplay.next_level_signal.connect(self.Window.new_level)
        self.gameplay.player_killed_signal.connect(self.Window.remove_player)
        self.gameplay.daemon = True
        self.gameplay.start()

    def start_command_parser(self):
        self.command_parser.start_game_signal.connect(self.start_game)
        self.command_parser.daemon = True
        self.command_parser.start()

    def start_ui_window(self, number_of_players):
        self.Window = ServerPrintModifier(number_of_players, self.server, self)
        self.setWindowTitle("PyGalagaServer")
        self.show()

    def paintEvent(self, event):
        current_frame = self.movie.currentPixmap()
        frame_rect = current_frame.rect()
        frame_rect.moveCenter(self.rect().center())
        if frame_rect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frame_rect.left(), frame_rect.top(), current_frame)

    def closeEvent(self, event):
        self.key_notifier.die()

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    def __update_position__(self, key):
        params = '{}:{}'.format(0, key)
        self.move_player_signal.emit(params)

