from PyQt5.QtCore import QSize, Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from threading import Lock
import time, threading

from Galaga.Scripts.print_modifier import PrintModifier, MoveModifer



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

    elif key == Qt.Key_Up:
        Gameplay.create_projectile(self, avatar1)

    elif key == Qt.Key_W:
        Gameplay.create_projectile(self, avatar2)

    elif key == Qt.Key_A:
        if avatar2.x() > 10:
            avatar2.move(avatar2.x() - 10, avatar2.y())

    elif key == Qt.Key_D:
        if avatar2.x() < 740:
            avatar2.move(avatar2.x() + 10, avatar2.y())



class Gameplay(QWidget, QObject):

    finished = pyqtSignal()
    projectile_list = []
    mutex = Lock()


    def __init__(self, parent=None):
        super(Gameplay, self).__init__(parent)
        thread = threading.Thread(target=self.enemies_movement)
        projectile_thread = threading.Thread(target=self.move_projectile)
        # make test_loop terminate when the user exits the window
        thread.daemon = True
        projectile_thread.deamon = True

        self.label_avatar1 = QLabel(self)
        self.label_avatar2 = QLabel(self)
        self.resize(QSize(800, 600))
        self.list = []
        self.init_ui()

        thread.start()
        projectile_thread.start()

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

    def create_projectile(self, avatar):
        pew = QPixmap("img/projectile.png")
        pew = pew.scaled(10, 10)
        self.projectile_label = QLabel(self)
        self.projectile_label.setPixmap(pew)
        self.projectile_label.move(avatar.x() + 20, avatar.y() - 20)
        self.projectile_list.append(self.projectile_label)
        self.projectile_label.show()


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

            time.sleep(0.3)

    def keyPressEvent(self, event):
        thread = threading.Thread(target=avatars_movement(self, event))
        thread.isDaemon()
        thread.start()


    def move_projectile(self):
        while True:
            if len(self.projectile_list) > 0:
                for i in range(len(self.projectile_list)):
                    if self.projectile_list[i].y() <= 0:
                        self.projectile_list[i].hide()
                    else:
                        self.projectile_list[i].move(self.projectile_list[i].x(), self.projectile_list[i].y() - 20)
                        self.check_collision(self.projectile_list[i])
                time.sleep(0.1)

    def check_collision(self, projectile):
        if projectile.isVisible() and projectile.y() < 160:
            for enemy in reversed(self.list):
                if enemy.isVisible() and projectile.y() <= enemy.y():
                    if enemy.x() + 50 >= projectile.x() and enemy.x() <= projectile.x():
                        enemy.hide()
                        projectile.hide()
                        break

    def __update_position__(self, key):

        self.movement.move_player(self.print.label_avatar1, self.print.label_avatar2, key)

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

        elif key == Qt.Key_Up:
            Gameplay.create_projectile(self, avatar1)

        elif key == Qt.Key_W:
            Gameplay.create_projectile(self, avatar2)

