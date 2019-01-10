from PyQt5.QtCore import QThread, pyqtSignal


class ServerMonitor(QThread):

    trigger_event_signal = pyqtSignal(str, str)

    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        self.listen_for_server()

    def listen_for_server(self):
        while True:
            text = ''
            bin = self.socket.recv(1024)
            text += str(bin, 'utf8')
            if text.__contains__('command-'):
                split = text.split('-')
                self.trigger_event_signal.emit(split[1], split[2])
            if text == 'disconnect':
                #remove socket later
                pass