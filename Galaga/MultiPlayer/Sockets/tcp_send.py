import socket
from PyQt5.QtCore import QThread


class TcpSend:

    def __init__(self, address, port):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))

    def send_msg(self, msg):
        data = self.socket.send(msg.encode('utf8'))
        return data, socket