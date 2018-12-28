from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading


class MyThread(QThread):
    mutex = Lock()
    bullet_mutex = Lock()
    print_mutex = Lock()
