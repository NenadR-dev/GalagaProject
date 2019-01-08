import sys
from Galaga.Scripts.key_notifier import KeyNotifier
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPainter, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
import socket


class Test(QMainWindow):

    HOST = '192.168.101.244'  # The remote host
    PORT = 50005  # The same port as used by the server

    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.resize(QSize(800, 600))
        self.show()
        self.key_notifier = KeyNotifier()
        self.key_notifier.start()

    def keyPressEvent(self, event):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            if event.key() == Qt.Key_Right:
                text2send = "right"
                print(text2send)
                s.sendall(text2send.encode('utf8'))
            if event.key() == Qt.Key_Left:
                text2send = "left"
                print(text2send)
                s.sendall(text2send.encode('utf8'))
            if event.key() == Qt.Key_Up:
                text2send = "up"
                print(text2send)
                s.sendall(text2send.encode('utf8'))
            if event.key() == Qt.Key_Down:
                text2send = "{0}".format(event.key())
                print(text2send)
                s.sendall(text2send.encode('utf8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Test()
    sys.exit(app.exec_())
