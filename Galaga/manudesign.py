# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menudesign.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.SinglePlayerBtn = QtWidgets.QPushButton(Form)
        self.SinglePlayerBtn.setGeometry(QtCore.QRect(200, 110, 331, 81))
        self.SinglePlayerBtn.setObjectName("SinglePlayerBtn")
        self.MultiPlayerBtn = QtWidgets.QPushButton(Form)
        self.MultiPlayerBtn.setGeometry(QtCore.QRect(200, 260, 331, 81))
        self.MultiPlayerBtn.setCheckable(False)
        self.MultiPlayerBtn.setAutoDefault(False)
        self.MultiPlayerBtn.setDefault(False)
        self.MultiPlayerBtn.setFlat(False)
        self.MultiPlayerBtn.setObjectName("MultiPlayerBtn")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 410, 331, 81))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.SinglePlayerBtn.setText(_translate("Form", "Single Player"))
        self.MultiPlayerBtn.setText(_translate("Form", "Multi Player"))
        self.pushButton.setText(_translate("Form", "Exit"))


