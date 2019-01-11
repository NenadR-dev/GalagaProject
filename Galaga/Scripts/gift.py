from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
import time, random

class Gift(QLabel):

    create_gifr_signal = pyqtSignal(QLabel)
    remove_gift_signal = pyqtSignal()

    def __init__(self, avatar, parent=None):
        QLabel.__init__(self, parent)
        self.avatar = avatar
        self.gift = QPixmap("img/present1.png")
        self.gift = self.gift.scaled(45, 45)
        self.move(random.randint(740, 10), 540)
        self.setPixmap(self.gift)
        self.show()

    def good_power(self):
        pass #TODO usporiti enemy-je

    def bad_power(self):
        pass #TODO usporiti avatara

    def check_collision(self):
        pass

    def generate_power(self):
        if random.randint(0, 1):
            self.bad_power()
        else:
            self.good_power()