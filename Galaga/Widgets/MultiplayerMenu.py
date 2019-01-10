from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QLineEdit
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize
from Galaga.Widgets import HostWidget
from Galaga import menu_design
from Galaga.MultiPlayer.Sockets import tcp_listen, tcp_send
from Galaga.MultiPlayer.Multiplayer_Widgets.ServerGameWidget import MainWindow
from Galaga.MultiPlayer.Scripts.socket_monitor import SocketMonitor
import socket


class Ui_Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window = self.setupUi(self)
        self.game = MainWindow()
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
                self.init_server_thread(tcp_send.TcpSend.socket)
            print(text)

    def init_server_thread(self, conn):
        self.server_listener = SocketMonitor(conn)
        self.server_listener.trigger_event_signal.connect(self.game.command_parser.parse_command)
        self.server_listener.daemon = True
        self.server_listener.start()
