from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QLabel
import time, random

class Gift(QThread):

    gift_start_signal = pyqtSignal()
    gift_remove_signal = pyqtSignal()
    stop_enemies_signal = pyqtSignal()

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

    @pyqtSlot()
    def good_power(self):
        self.stop_enemies_signal.emit()
