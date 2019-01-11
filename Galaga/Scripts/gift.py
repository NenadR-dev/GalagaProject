from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
import time, random

class Gift(QThread):

    gift_start_signal = pyqtSignal()
    gift_remove_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.gift_clock()

    def gift_clock(self):
        time.sleep(1)
        while True:
            time.sleep(7)
            self.gift_start_signal.emit()
            time.sleep(4)
            self.gift_remove_signal.emit()

    def good_power(self, avatar):
        pass #TODO usporiti enemy-je

    def bad_power(self):
        pass #TODO usporiti avatara
