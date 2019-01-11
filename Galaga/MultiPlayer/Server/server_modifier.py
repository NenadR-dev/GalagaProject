from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, Qt
from Galaga.MultiPlayer.Common.host_data import HostData
from Galaga.MultiPlayer.Sockets import tcp_listen, tcp_send
from threading import Lock

class ServerModifer(QThread):

    def __init__(self):
        super(ServerModifer, self).__init__()
        self.mutex = Lock()
    def run(self):
        print('server modifier up and running')

    def send_command(self, command):
        self.mutex.acquire()
        for node in HostData.client_address:
            HostData.client_address[node].send(command.encode('utf8'))
        self.mutex.release()

