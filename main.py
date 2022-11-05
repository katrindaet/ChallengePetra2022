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

        text_font = QFont("Arial", 16)
        display_font = QFont("Arial", 20)
        # change the font of the textedit
        self.textEdit.setFont(display_font)
        # max size of the textedit
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 450))


        for i in range(12):
            b1 = QPushButton("Suggestions")
            b1.setFont(text_font)
            # make the buttom expand
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            y = i % 3
            x = math.floor(i/3)
            self.gridLayout1.addWidget(b1,x,y)
        for i in range(6):
            b1 = QPushButton("Themes")
            b1.setFont(text_font)
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            b1.setMaximumWidth(300)

            y = i % 2
            x = math.floor(i/2)
            self.gridLayout2.addWidget(b1,x,y)
        for i in range(4):
            b1 = QPushButton("Custom")
            b1.setFont(text_font)
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # max width of the button
            b1.setMaximumWidth(300)

            y = i % 2
            x = math.floor(i/2)
            self.gridLayout3.addWidget(b1,x,y)

        # add icons in settings
        icon = QIcon(".\icons_gui\delete.png")
        self.Setting2.setIcon(icon)
        icon = QIcon(".\icons_gui\close.png")
        self.Setting3.setIcon(icon)
        icon = QIcon(".\icons_gui\\frame.png")
        # icon = QIcon(".\icons_gui\frame.png")
        self.Setting4.setIcon(icon)
        icon = QIcon(".\icons_gui\plus.png")
        self.Setting5.setIcon(icon)
        icon = QIcon(".\icons_gui\settings.png")
        self.Setting6.setIcon(icon)
        icon = QIcon(".\icons_gui\speaker.png")
        self.Setting1.setIcon(icon)

        # loop through Setting1 to 6 and make the botton expand
        for i in range(6):
            b1 = getattr(self, "Setting" + str(i+1))
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            b1.setMaximumWidth(300)
    

        # adapt size of icon
        self.Setting2.setIconSize(QtCore.QSize(100, 100))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



# convert gui.ui to .py
# pyuic5 gui.ui -o gui.py
