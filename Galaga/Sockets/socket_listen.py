# Echo server program
import socket
from Galaga.Scripts.my_thread import MyThread
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, Qt
import time


class Socket_Listen(QThread):

    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50005  # Arbitrary non-privileged port
    move_player_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

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
                            self.move_player_signal.emit(Qt.Key_A)
                        if text == 'right':
                            self.move_player_signal.emit(Qt.Key_D)
                        if text == 'up':
                            self.move_player_signal.emit(Qt.Key_W)
                        text = ''