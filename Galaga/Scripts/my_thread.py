from PyQt5.QtCore import QThread
from threading import Lock


class MyThread(QThread):
    mutex = Lock()
    projectile_mutex = Lock()
    gameplay_lock = Lock()
