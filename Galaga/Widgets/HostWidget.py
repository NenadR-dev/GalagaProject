from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QMovie, QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize
from Galaga.Widgets import GameWidget
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
        self.startBtn = QtWidgets.QPushButton(Form)
        self.startBtn.setGeometry(QtCore.QRect(200, 300, 331, 81))
        self.startBtn.setObjectName("Start")
        self.startBtn.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")

        #set label
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(200,50,331,81))
        self.label1.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")
        self.label1.setText('Connected players: ')

        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(200,120,331,81))
        self.label2.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")
        self.label2.setText('0')

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Galaga"))
        Form.setWindowIcon(QIcon("img/avatar1.png"))

        self.startBtn.setText(_translate("Form", "Start"))
        self.startBtn.clicked.connect(self.startBtn_press)

    def startBtn_press(self):
        pass



