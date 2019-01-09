from PyQt5.QtCore import QThread
from threading import Lock


class CommonThread(QThread):
    mutex_movement = Lock()
    mutex_send_signal = Lock()

    def __init__(self):
        print('Common thread up and running')