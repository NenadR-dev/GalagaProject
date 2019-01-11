from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap


class Avatar(QLabel):

    avatar_num = 1
    position = 740

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        avatar = QPixmap("img/avatar{}.png".format(Avatar.avatar_num))
        print("img/avatar{}.png".format(Avatar.avatar_num))
        avatar = avatar.scaled(50, 50)
        self.index = Avatar.avatar_num
        Avatar.avatar_num += 1
        self.setPixmap(avatar)
        self.move(Avatar.position, 540)
        Avatar.position -= 730
        self.show()

    def set_position(self, x):
        self.move(x, 540)