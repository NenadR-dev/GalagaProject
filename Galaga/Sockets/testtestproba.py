import sys
from Galaga.Scripts.key_notifier import KeyNotifier
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import socket
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QLineEdit
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize
from Galaga.Widgets import HostWidget
from Galaga import menu_design
from Galaga.MultiPlayer.Sockets import tcp_send


class Test(QMainWindow):

    HOST = '127.0.0.1'  # The remote host
    PORT = 50005  # The same port as used by the server

    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.resize(QSize(800, 600))
        self.show()
        self.key_notifier = KeyNotifier()
        self.key_notifier.start()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.socket.sendall('123'.encode('utf8'))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            text2send = "right"
            print(text2send)
            self.socket.sendall(text2send.encode('utf8'))
        if event.key() == Qt.Key_Left:
            text2send = "left"
            print(text2send)
            self.socket.sendall(text2send.encode('utf8'))
        if event.key() == Qt.Key_Up:
            text2send = "up"
            print(text2send)
            self.socket.sendall(text2send.encode('utf8'))
        if event.key() == Qt.Key_Down:
            text2send = "{0}".format(event.key())
            print(text2send)
            self.socket.sendall(text2send.encode('utf8'))


class Ui_Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window = self.setupUi(self)
        self.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setGeometry(0, 0, 800, 600)
        Form.setFixedSize(800, 600)

        #set background
        oImage = QImage("img/space-background.gif")
        sImage = oImage.scaled(QSize(800, 600))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        #set buttons
        self.HostBtn = QtWidgets.QPushButton(Form)
        self.HostBtn.setGeometry(QtCore.QRect(200, 110, 331, 81))
        self.HostBtn.setObjectName("HostBtn")
        self.HostBtn.setStyleSheet('background-color: #1e3962; color: white; font: italic; font-size: 30px;')

        self.JoinBtn = QtWidgets.QPushButton(Form)
        self.JoinBtn.setGeometry(QtCore.QRect(200, 260, 331, 81))
        self.JoinBtn.setObjectName("JoinBtn")
        self.JoinBtn.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")

        self.waiting = QtWidgets.QLabel(Form)
        self.waiting.setGeometry(QtCore.QRect(200, 260, 331, 81))
        self.waiting.setObjectName("waiting")
        self.waiting.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")
        self.waiting.hide()


        self.backBtn = QtWidgets.QPushButton(Form)
        self.backBtn.setGeometry(QtCore.QRect(200, 410, 331, 81))
        self.backBtn.setObjectName("backBtn")
        self.backBtn.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Galaga"))
        Form.setWindowIcon(QIcon("img/avatar1.png"))
        self.HostBtn.setText(_translate("Form", "Host game"))
        self.HostBtn.clicked.connect(self.host_btn_press)

        self.JoinBtn.setText(_translate("Form", "Join game"))
        self.JoinBtn.clicked.connect(self.join_btn_press)

        self.waiting.setText(_translate("Form", "\tWaiting"))

        self.backBtn.setText(_translate("Form", "Back"))
        self.backBtn.clicked.connect(self.back_button_press)

    def back_button_press(self):
        self.window = menu_design.Ui_Form()
        self.close()

    def host_btn_press(self):
        self.window = HostWidget.Ui_Form()
        self.close()

    def join_btn_press(self):
        self.HostBtn.hide()
        self.JoinBtn.hide()
        self.backBtn.hide()
        self.get_host_ip()
        self.waiting.show()

    def get_host_ip(self):
        text, okPressed = QInputDialog.getText(self, "Insert Host IP", "IP:", QLineEdit.Normal, "")
        if okPressed and text != '':
            bytes_sent = tcp_send.TcpSend(text, 50005).send_msg('new_player')
            if bytes_sent > 0:
                self.waiting.setText(QtCore.QCoreApplication.translate("Form", "Connected"))
            print(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Ui_Form()
    sys.exit(app.exec_())
