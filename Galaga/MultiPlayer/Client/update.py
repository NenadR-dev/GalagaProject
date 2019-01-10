from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, Qt


class Update(QThread):

    def __init__(self):
        super().__init__()

    def run(self):
        print('update running')
