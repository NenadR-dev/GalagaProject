from Galaga.MultiPlayer.Common.common_thread import CommonThread
from Galaga.MultiPlayer.Common.host_modifier import HostData
from  PyQt5.QtCore import pyqtSignal, QThread
import  socket


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