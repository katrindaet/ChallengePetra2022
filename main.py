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
import tts

# .setMaximumSize(QtCore.QSize(16777215, 80))

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mytts = tts.TTS()
        text_font = QFont("Arial", 20)
        display_font = QFont("Arial", 24)
        # set font color
        text_font.setBold(True)
        display_font.setBold(True)

        # change the font of the textedit
        self.textEdit.setFont(display_font)
        # max size of the textedit
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 450))

        for i in range(12):
            b1 = QPushButton("Suggestions")
            b1.setFont(text_font)
            # make the buttom expand
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # background color of the buttom
            b1.setStyleSheet("background-color: rgb(120, 120, 120);")
            y = i % 3
            x = math.floor(i/3)
            self.gridLayout1.addWidget(b1,x,y)

            # when b1 is clicked append vertically the name of the botton in the textedit
            b1.clicked.connect(lambda state, b1=b1: self.textEdit.append(b1.text()))


        for i in range(6):
            b1 = QPushButton("Themes")
            b1.setFont(text_font)
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            b1.setMaximumWidth(300)
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout2.addWidget(b1,x,y)
            
            # background color of the buttom
            b1.setStyleSheet("background-color: rgb(0, 60, 120);")

        for i in range(4):
            b1 = QPushButton("Custom")
            b1.setFont(text_font)
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # max width of the button
            b1.setMaximumWidth(300)

            y = i % 2
            x = math.floor(i/2)
            self.gridLayout3.addWidget(b1,x,y)

            # background color of the buttom
            b1.setStyleSheet("background-color: rgb(120, 60, 0);")

        # add icons in settings
        icon = QIcon(".\icons_gui\delete.png")
        self.Setting2.setIcon(icon)
        icon = QIcon(".\icons_gui\close.png")
        self.Setting3.setIcon(icon)
        icon = QIcon(".\icons_gui\\frame.png")
        self.Setting4.setIcon(icon)
        icon = QIcon(".\icons_gui\plus.png")
        self.Setting5.setIcon(icon)
        icon = QIcon(".\icons_gui\settings.png")
        self.Setting6.setIcon(icon)
        icon = QIcon(".\icons_gui\speaker.png")
        self.Setting1.setIcon(icon)
        # when setting1 is clicked print the content of textedit in the console
        self.Setting1.clicked.connect(lambda state, self=self: self.mytts.say(self.textEdit.toPlainText()))
        # > mytts = tts.TTS()
# > mytts.say('Hello, World')
        # loop through Setting1 to 6 and make the botton expand
        for i in range(6):
            b1 = getattr(self, "Setting" + str(i+1))
            b1.setIconSize(QSize(200,200))
            # set minimum size of the button
            b1.setMinimumSize(QSize(100,100))
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            b1.setMaximumWidth(300)


        # when any botton is pressed do something

        # adapt size of icon
        self.Setting2.setIconSize(QtCore.QSize(100, 100))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



# convert gui.ui to .py
# pyuic5 gui.ui -o gui.py
