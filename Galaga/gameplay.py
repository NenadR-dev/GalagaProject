from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
import time, threading

def avatars_movement(self, event):
    avatar1 = self.label_avatar1
    avatar2 = self.label_avatar2
    key = event.key()

    if key == Qt.Key_Left:
        if avatar1.x() > 10:
            avatar1.move(avatar1.x() - 10, avatar1.y())

    elif key == Qt.Key_Right:
        if avatar1.x() < 740:
            avatar1.move(avatar1.x() + 10, avatar1.y())

    elif key == Qt.Key_A:
        if avatar2.x() > 10:
            avatar2.move(avatar2.x() - 10, avatar2.y())

    elif key == Qt.Key_D:
        if avatar2.x() < 740:
            avatar2.move(avatar2.x() + 10, avatar2.y())



class Gameplay(QWidget, QObject):

    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(Gameplay, self).__init__(parent)
        thread = threading.Thread(target=self.enemies_movement)
        # make test_loop terminate when the user exits the window
        thread.daemon = True

        self.label_avatar1 = QLabel(self)
        self.label_avatar2 = QLabel(self)
        self.resize(QSize(800, 600))
        self.list = []
        self.init_ui()

        thread.start()

    def init_ui(self):
        avatar1 = QPixmap("img/avatar.png")
        avatar1 = avatar1.scaled(50, 50)
        self.label_avatar1.setPixmap(avatar1)
        self.label_avatar1.move(10, 540)

        avatar2 = QPixmap("img/avatar2.png")
        avatar2 = avatar2.scaled(50, 50)
        self.label_avatar2.setPixmap(avatar2)
        self.label_avatar2.move(740, 540)

        for i in range(0, 10):
            for j in range(0, 3):
                label_enemy = QLabel(self)
                enemy = QPixmap("img/enemy.png")
                enemy = enemy.scaled(50, 50)
                label_enemy.setPixmap(enemy)
                label_enemy.move(150 + i*50, 10 + j*50)
                self.list.append(label_enemy)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('PyGalaga')
        self.show()

    def start_thread(self):
        self.thread.start()

    @pyqtSlot()
    def enemies_movement(self):
        direction = "left"
        while True:
            if direction == "left":
                for i in range(30):
                    self.list[i].move(self.list[i].x() - 10, self.list[i].y())
                if self.list[0].x() == 10:
                    direction = "right"
            elif direction == "right":
                for i in range(30):
                    self.list[i].move(self.list[i].x() + 10, self.list[i].y())
                if self.list[29].x() == 740:
                    direction = "left"
            time.sleep(0.8)

    def __update_position__(self, key):
        avatar1 = self.label_avatar1
        avatar2 = self.label_avatar2

        if key == Qt.Key_Left:
            if avatar1.x() > 10:
                avatar1.move(avatar1.x() - 10, avatar1.y())

        elif key == Qt.Key_Right:
            if avatar1.x() < 740:
                avatar1.move(avatar1.x() + 10, avatar1.y())

        elif key == Qt.Key_A:
            if avatar2.x() > 10:
                avatar2.move(avatar2.x() - 10, avatar2.y())

        elif key == Qt.Key_D:
            if avatar2.x() < 740:
                avatar2.move(avatar2.x() + 10, avatar2.y())
