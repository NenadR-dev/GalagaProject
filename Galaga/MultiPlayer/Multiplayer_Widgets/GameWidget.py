from PyQt5.QtGui import QMovie, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from Galaga.MultiPlayer.Scripts.command_parser import CommandParser


class MainWindow(QWidget):

    move_player_signal = pyqtSignal(int)
    command_parser = CommandParser()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.start_command_parser()

    @pyqtSlot(int)
    def start_game(self, number_of_players):
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)
        self.start_ui_window()

        self.movie = QMovie("img/space-background.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def start_command_parser(self):
        self.command_parser.start_game_signal.connect(self.start_game)
        self.command_parser.daemon = True
        self.command_parser.start()

    def start_ui_window(self):
        #self.Window = PrintModifier(self)
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

