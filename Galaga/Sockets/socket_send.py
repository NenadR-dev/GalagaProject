import sys
from Galaga.Scripts.key_notifier import KeyNotifier
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie, QPainter, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
import socket

HOST = '192.168.101.244'  # The remote host
PORT = 50005  # The same port as used by the server


def send(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(text.encode('utf8'))