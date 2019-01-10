from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from Galaga.MultiPlayer.Scripts.command_parser import CommandParser
from Galaga.MultiPlayer.Scripts.multiplayer_print_modifier import MultiplayerPrintModifier
from Galaga.MultiPlayer.multiplayer_gameplay import Gameplay
from Galaga.Scripts.key_notifier import KeyNotifier
from Galaga.MultiPlayer.Sockets.tcp_send import TcpSend
from Galaga.MultiPlayer.Common.client_data import ClientData
from Galaga.MultiPlayer.Client.client_move_modifier import ClientMultiplayerMoveModifer


class ClientMainWindow(QWidget):

    command_parser = CommandParser()
    move_player_signal = pyqtSignal(int,int)

    def __init__(self, parent=None):
        super(ClientMainWindow, self).__init__(parent)
        self.start_command_parser()

    @pyqtSlot(int)
    def start_game(self, number_of_players):
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)

        self.start_ui_window(number_of_players)
        self.start_gameplay(number_of_players)
        self.start_key_notifier()

        #set gif animation
        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        self.start_movement()

    def start_movement(self):
        self.movement = ClientMultiplayerMoveModifer(self.Window)
        self.move_player_signal.connect(self.player_movement.move_player)
        self.movement.move_player_signal.connect(self.Window.move_player)
        self.movement.create_projectile_signal.connect(self.Window.print_projectile)
        self.movement.move_enemy_signal.connect(self.Window.move_enemy)
        self.movement.enemy_kamikaze_signal.connect(self.Window.enemy_move_attack)
        self.movement.daemon = True
        self.movement.start()

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
        self.command_parser.move_player_signal.connect(self.Window.move_player)
        self.command_parser.fire_projectile_signal.connect(self.Window.print_projectile)
        self.command_parser.move_enemy_signal.connect(self.movement.move_enemy)
        self.command_parser.move_projectile_signal.connect(self.movement.move_projectile)
        self.command_parser.remove_projectile_signal.connect(self.Window.remove_projectile)
        self.command_parser.remove_enemy_signal.connect(self.Window.remove_enemy)
        self.command_parser.enemy_kamikaze_signal.connect(self.movement.enemy_kamikaze)
        self.command_parser.enemy_projectile_attack_signal.connect(self.Window.enemy_projectile_attack)
        self.command_parser.remove_player_signal.connect(self.Window.remove_player)
        self.command_parser.daemon = True
        self.command_parser.start()

    def start_ui_window(self, number_of_players):
        self.Window = MultiplayerPrintModifier(number_of_players)
        self.setWindowTitle("PyGalaga")
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
        self.move_player(key)

    #salje serveru
    def move_player(self, key):
        if key == Qt.Key_Left:
            self.move_player_signal.emit(key, ClientData.client_id)
            TcpSend.send_msg(msg='{}-{}-{}'.format('command', ClientData.client_id, key))
        elif key == Qt.Key_Right:
            self.move_player_signal.emit(key, ClientData.client_id)
            TcpSend.send_msg(msg='{}-{}-{}'.format('command', ClientData.client_id, key))
        elif key == Qt.Key_Up:
            self.move_player_signal.emit(key, ClientData.client_id)
            TcpSend.send_msg(msg='{}-{}-{}'.format('command', ClientData.client_id, key))