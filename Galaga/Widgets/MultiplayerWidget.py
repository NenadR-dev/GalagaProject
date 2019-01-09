from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QMovie, QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize


class MultiPlayer(QWidget):

    def __init__(self):
        super(self).__init__()
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
        self.SinglePlayerBtn = QtWidgets.QPushButton(Form)
        self.SinglePlayerBtn.setGeometry(QtCore.QRect(200, 110, 331, 81))
        self.SinglePlayerBtn.setObjectName("Create")
        self.SinglePlayerBtn.setStyleSheet('background-color: #1e3962; color: white; font: italic; font-size: 30px;')

        self.MultiPlayerBtn = QtWidgets.QPushButton(Form)
        self.MultiPlayerBtn.setGeometry(QtCore.QRect(200, 260, 331, 81))
        self.MultiPlayerBtn.setObjectName("Join")
        self.MultiPlayerBtn.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")

        self.exitBtn = QtWidgets.QPushButton(Form)
        self.exitBtn.setGeometry(QtCore.QRect(200, 410, 331, 81))
        self.exitBtn.setObjectName("Return")
        self.exitBtn.setStyleSheet("background-color: #1e3962; color: white; font: italic; font-size: 30px;")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Galaga"))
        Form.setWindowIcon(QIcon("img/avatar1.png"))
        self.SinglePlayerBtn.setText(_translate("Form", "Single Player"))
        self.SinglePlayerBtn.clicked.connect(self.single_player_btn_press)

        self.MultiPlayerBtn.setText(_translate("Form", "Multi Player"))
        self.MultiPlayerBtn.clicked.connect(self.multi_player_btn_press)

        self.exitBtn.setText(_translate("Form", "Exit"))
        self.exitBtn.clicked.connect(self.exit_button_press)

    def exit_button_press(self):
        self.close()
        self.window =

    def single_player_btn_press(self):
        self.window = GameWidget.MainWindow()
        self.close()

    def multi_player_btn_press(self):
        self.setLayout(MultiplayerWidget)
        self.close()

