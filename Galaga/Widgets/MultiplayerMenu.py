from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QMovie, QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize
from Galaga.Widgets import HostWidget, GameWidget
from Galaga import menu_design


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

        self.backBtn.setText(_translate("Form", "Back"))
        self.backBtn.clicked.connect(self.back_button_press)

    def back_button_press(self):
        self.window = menu_design.Ui_Form()
        self.close()

    def host_btn_press(self):
        self.window = HostWidget.Ui_Form()
        self.close()

    def join_btn_press(self):
        pass



