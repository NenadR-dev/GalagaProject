from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from Galaga.MultiPlayer.Scripts.command_parser import CommandParser
from Galaga.MultiPlayer.Client.client_print_modifier import ClientPrintModifier
from Galaga.MultiPlayer.multiplayer_gameplay import Gameplay
from Galaga.Scripts.key_notifier import KeyNotifier
from Galaga.MultiPlayer.Sockets.tcp_send import TcpSend
from Galaga.MultiPlayer.Common.client_data import ClientData
from Galaga.MultiPlayer.Client.client_move_modifier import ClientMoveModifier


class ClientMainWindow(QWidget):

    command_parser = CommandParser()


    def __init__(self, tcp_socket, parent=None):
        super(ClientMainWindow, self).__init__(parent)
        self.command_parser.start_game_signal.connect(self.start_game)
        self.command_parser.daemon = True
        self.command_parser.start()
        self.tcp = tcp_socket
    @pyqtSlot(str)
    def start_game(self, params):
        self.param = params.split(':')
        self.player_count = int(self.param[0])
        ClientData.client_id = int(self.param[1])
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)

        self.start_ui_window(self.player_count)
        self.start_command_parser()
        self.start_key_notifier()

        #set gif animation
        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        #self.start_movement()

    '''def start_movement(self):
        self.movement = ClientMoveModifier(self.Window)
        self.movement.move_player_signal.connect(self.Window.move_player)
        self.movement.create_projectile_signal.connect(self.Window.print_projectile)
        self.movement.move_enemy_signal.connect(self.Window.move_enemy)
        self.movement.enemy_kamikaze_signal.connect(self.Window.enemy_move_attack)
        self.movement.daemon = True
        self.movement.start()'''

    def start_key_notifier(self):
        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def start_command_parser(self):
        self.command_parser.move_player_signal.connect(self.Window.move_player)
        self.command_parser.fire_projectile_signal.connect(self.Window.print_projectile)
        self.command_parser.move_enemy_signal.connect(self.Window.move_enemy)
        self.command_parser.move_projectile_signal.connect(self.Window.move_projectile)
        self.command_parser.remove_projectile_signal.connect(self.Window.remove_projectile)
        self.command_parser.remove_enemy_signal.connect(self.Window.remove_enemy)
        #self.command_parser.enemy_kamikaze_signal.connect(self.Window.enemy_move_attack)
        self.command_parser.enemy_projectile_attack_signal.connect(self.Window.enemy_projectile_attack)
        self.command_parser.remove_player_signal.connect(self.Window.remove_player)


    def start_ui_window(self, number_of_players):
        self.Window = ClientPrintModifier(number_of_players, self)
        self.setWindowTitle("PyGalagaClient")
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
            print('{}-{}-move_player'.format('command', ClientData.client_id))
            self.tcp.send('command-{}:{}-move_player'.format(ClientData.client_id, key).encode('utf8'))
        elif key == Qt.Key_Right:
            print('{}-{}-move_player'.format('command', ClientData.client_id))
            self.tcp.send('command-{}:{}-move_player'.format(ClientData.client_id, key).encode('utf8'))
        elif key == Qt.Key_Up:
            print('{}-{}-create_projectile'.format('command', ClientData.client_id))
            self.tcp.send('command-{}-create_projectile'.format(ClientData.client_id).encode('utf8'))