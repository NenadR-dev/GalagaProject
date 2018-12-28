import sys
from PyQt5.QtGui import QMovie, QPainter
<<<<<<< HEAD
from PyQt5.QtWidgets import QApplication, QMainWindow

from Galaga.Scripts.print_modifier import PrintModifier
from Galaga.Scripts.move_modifier import MoveModifer

from Galaga.gameplay import Gameplay
from Galaga.Scripts.key_notifier import KeyNotifier

=======
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import pyqtSlot
>>>>>>> cdb5bf4bccfa9cbf278418b1ef9a05fe56dcf808
from Galaga.gameplay import Gameplay
from Galaga.Scripts.key_notifier import KeyNotifier
from Galaga.Scripts.print_modifier import PrintModifier
from Galaga.Scripts.move_modifier import MoveModifer
from gameplay import Gameplay
from Scripts.key_notifier import KeyNotifier
from Scripts.projectile_modifier import ProjectileModifier

<<<<<<< HEAD
=======
import threading
import time
>>>>>>> cdb5bf4bccfa9cbf278418b1ef9a05fe56dcf808

class MainWindow(QMainWindow):


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)
        self.start_ui_window()

        #set gif background
        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        #set key notifiers
        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        #set projectiles
        self.projectiles = ProjectileModifier(self.Window.local_enemy_list, self.Window)
        self.projectiles.projectile_move_signal.connect(self.Window.move_projectile)
        self.Window.move_p.connect(self.projectiles.add_projectile)
        self.Window.daemon = True
        self.projectiles.start()

        #set player movement
        self.movement = MoveModifer(self.Window.local_enemy_list, self.Window)
        self.movement.create_projectile_signal.connect(self.Window.print_projectile)
        self.movement.move_player_signal.connect(self.Window.move_player)
        self.movement.move_enemy_signal.connect(self.Window.move_enemy)
        self.movement.daemon = True
        self.movement.start()


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
        self.movement.move_player(key)
        #Gameplay.__update_position__(self.Window, key)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())