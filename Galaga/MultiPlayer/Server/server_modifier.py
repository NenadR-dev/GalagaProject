from PyQt5.QtCore import QThread
from Galaga.MultiPlayer.Common.host_data import HostData
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

