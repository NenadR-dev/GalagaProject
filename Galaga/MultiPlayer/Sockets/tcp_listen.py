# Echo server program
import socket
from PyQt5.QtCore import QThread, pyqtSignal
from Galaga.MultiPlayer.Common.host_data import HostData
from Galaga.MultiPlayer.Scripts.socket_monitor import SocketMonitor


class TcpListen(QThread):

    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50005  # Arbitrary non-privileged port

    update_client_num_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        self.listen()

    def listen(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                s.listen(1)
                conn, addr = s.accept()
                print('Connected by', addr)
                text = ''
                bin = conn.recv(1024)
                text += str(bin, 'utf8')
                if len(text) > 0:
                    if text == 'new_player':
                        HostData.connected_client += 1
                        HostData.client_address[addr] = conn
                        self.update_client_num_signal.emit(HostData.connected_client)
                        socket_monitor = SocketMonitor(conn)
                        socket_monitor.daemon = True
<<<<<<< HEAD
                        socket_monitor.start()
=======
                        socket_monitor.start()
>>>>>>> 1b6d25ef4c7f7204fce3daa525445282e9ba8dc4
