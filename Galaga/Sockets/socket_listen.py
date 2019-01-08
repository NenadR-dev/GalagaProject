# Echo server program
import socket
from Galaga.Scripts.my_thread import MyThread
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, Qt

class Socket_Listen(MyThread):

    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50005  # Arbitrary non-privileged port
    move_player_signal = pyqtSignal()
    def __init__(self, move_modifier):
        super().__init__()
        self.move = move_modifier

    def run(self):
        self.listen()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                text = ''
                while True:
                    bin = conn.recv(1024)
                    text += str(bin, 'utf8')
                    if len(text) > 0:
                        if text == 'left':
                            self.move.move_player(Qt.Key_A)
                        if text == 'right':
                            self.move.move_player(Qt.Key_D)
                        if text == 'up':
                            self.move.move_player(Qt.Key_W)
