import sys
import math
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
# import Qfont
from PyQt5.QtGui import QFont

from GUI import Ui_MainWindow

# .setMaximumSize(QtCore.QSize(16777215, 80))

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        font = 16


        for i in range(10):
            b1 = QPushButton("Button1")
            b1.setFont(QFont("Arial", font))
            # make the buttom
            y = i % 3
            x = math.floor(i/3)
            self.gridLayout1.addWidget(b1,x,y)
        for i in range(6):
            b1 = QPushButton("Button1")
            b1.setFont(QFont("Arial", font))
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout2.addWidget(b1,x,y)
        for i in range(4):
            b1 = QPushButton("Button1")
            b1.setFont(QFont("Arial", font))
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout3.addWidget(b1,x,y)

        # add icons in settings
        icon = QIcon(".\icons_gui\delete.png")
        self.Setting2.setIcon(icon)
        # adapt size of icon
        self.Setting2.setIconSize(QtCore.QSize(100, 100))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



# convert gui.ui to .py
# pyuic5 gui.ui -o gui.py
