import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from Galaga.menu_design import Ui_Form


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Ui_Form()
    sys.exit(app.exec_())