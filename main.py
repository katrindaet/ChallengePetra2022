import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from GUI import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        for i in range(10):
            b1 = QPushButton("Button1")
            y = i % 3
            x = math.floor(i/3)
            self.gridLayout1.addWidget(b1,x,y)
        for i in range(6):
            b1 = QPushButton("Button1")
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout2.addWidget(b1,x,y)
        for i in range(4):
            b1 = QPushButton("Button1")
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout3.addWidget(b1,x,y)

        # add icons in settings
        icon = QIcon(".\icons_gui\delete.png")
        self.Setting2.setIcon(icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



# convert gui.ui to .py
# pyuic5 gui.ui -o gui.py
