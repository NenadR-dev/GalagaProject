from Galaga.MultiPlayer.Common.common_thread import CommonThread
<<<<<<< HEAD
from Galaga.MultiPlayer.Common.host_data import HostData
from  PyQt5.QtCore import pyqtSignal, QThread
import socket
=======
from Galaga.MultiPlayer.Common.host_modifier import HostData
from  PyQt5.QtCore import pyqtSignal, QThread
import  socket
>>>>>>> 1b6d25ef4c7f7204fce3daa525445282e9ba8dc4


class SocketMonitor(QThread):

    trigger_event_signal = pyqtSignal(str, str)

    def __init__(self, socket):
        super().__init__()
        self.active_socket = socket

    def run(self):
        self.listen_for_activity()

    def listen_for_activity(self):
        while True:
            text = ''
            bin = self.active_socket.recv(1024)
            text += str(bin, 'utf8')
            if text.__contains__('command-'):
                split = text.split('-')
                self.trigger_event_signal.emit(split[1], split[2])
            if text == 'disconnect':
                #remove socket later
                pass