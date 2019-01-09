import sys
from Galaga.Scripts.print_modifier import PrintModifier
from Galaga.Scripts.move_modifier import MoveModifer
from Galaga.Scripts.key_notifier import KeyNotifier
from Galaga.Scripts.projectile_modifier import ProjectileModifier, EnemyProjectileModifier
from Galaga.Scripts.enemy_attacks import EnemyMoveAttack, EnemyProjectileAttack
from Galaga.gameplay import Gameplay
from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QWidget
from Galaga.Sockets import socket_listen, socket_send
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot


class MainWindow(QWidget):

    move_player_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)
        self.start_ui_window()
        self.gameplay = Gameplay()

        # set game logic
        self.gameplay.next_level_signal.connect(self.Window.new_level)
        self.gameplay.player_killed_signal.connect(self.Window.remove_player)
        self.gameplay.daemon = True
        self.gameplay.start()

        # set gif background
        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        # set key notifiers
        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        # set projectiles
        self.projectiles = ProjectileModifier(self.Window.local_enemy_list, self.Window, self.gameplay)
        self.projectiles.projectile_move_signal.connect(self.Window.move_projectile)
        self.projectiles.projectile_remove_signal.connect(self.Window.remove_projectile)
        self.projectiles.enemy_killed_signal.connect(self.Window.remove_enemy)
        self.Window.move_p.connect(self.projectiles.add_projectile)
        self.Window.count_enemy_signal.connect(self.gameplay.count_killed_enemies)
        self.Window.remove_enemy_projectile_signal.connect(self.projectiles.remove_projectiles)
        self.Window.daemon = True
        self.projectiles.start()

        self.enemy_projectiles = EnemyProjectileModifier(self.Window.label_avatar1, self.Window.label_avatar2, self.Window, self.gameplay)
        self.enemy_projectiles.projectile_move_signal.connect(self.Window.move_enemy_projectile)
        self.Window.move_enemy_p.connect(self.enemy_projectiles.add_projectile)
        self.Window.remove_enemy_projectile_signal.connect(self.projectiles.remove_projectiles)
        self.enemy_projectiles.projectile_remove_signal.connect(self.Window.remove_projectile)
        self.enemy_projectiles.player_hit_signal.connect(self.gameplay.player_hit)
        self.enemy_projectiles.daemon = True
        self.enemy_projectiles.start()

        # set movement
        self.movement = MoveModifer(self.Window.local_enemy_list, self.Window, self.gameplay)
        self.movement.create_projectile_signal.connect(self.Window.print_projectile)
        self.movement.move_player_signal.connect(self.Window.move_player)
        self.movement.move_enemy_signal.connect(self.Window.move_enemy)
        self.move_player_signal.connect(self.movement.move_player)
        self.movement.daemon = True
        self.movement.start()

        self.socket = socket_listen.Socket_Listen()
        self.socket.move_player_signal.connect(self.movement.move_player)
        self.socket.daemon = True
        self.socket.start()

        #TODO STEFANJE NE RADI TI KAKO TREBA ENEMY ATTACK TU NEGDE PUCA

        # set enemy attacks
        self.enemy_move_attack = EnemyMoveAttack(self.Window.local_enemy_list, self.Window.label_avatar1,
                                              self.Window.label_avatar2, self.gameplay)
        self.enemy_move_attack.enemy_attack_move_signal.connect(self.Window.enemy_move_attack)
        self.enemy_move_attack.return_enemy_signal.connect(self.Window.return_enemy)
        self.enemy_move_attack.player_hit_singal.connect(self.gameplay.player_hit)
        self.enemy_move_attack.daemon = True
        self.enemy_move_attack.start()

        self.enemy_projectile_attack = EnemyProjectileAttack(self.Window.local_enemy_list, self.Window.label_avatar1,
                                                 self.Window.label_avatar2)
        self.enemy_projectile_attack.enemy_attack_projectile_signal.connect(self.Window.enemy_projectile_attack)
        self.enemy_projectile_attack.daemon = True
        self.enemy_projectile_attack.start()

    def start_ui_window(self):
        self.Window = PrintModifier(self)
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
        self.move_player_signal.emit(key)

