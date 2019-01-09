from PyQt5.QtCore import QThread
from threading import Lock


class MyThread(QThread):
    def __init__(self):
        print("MyThread")

    mutex = Lock()
    projectile_mutex = Lock()
    gameplay_lock = Lock()