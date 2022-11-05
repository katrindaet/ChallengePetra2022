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
from database import Database

# detect when enter is pressed


# .setMaximumSize(QtCore.QSize(16777215, 80)

class MyButton(QPushButton):

    rightclick = pyqtSignal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        # self.setText(text)
        

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            #do what you want here
            print("Right Button Clicked")
            self.rightclick.emit()
        else:
            super().mousePressEvent(QMouseEvent)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mytts = tts.TTS()
        self.text_font = QFont("Arial", 20)
        self.display_font = QFont("Arial", 24)
        # set font color
        self.text_font.setBold(True)
        self.display_font.setBold(True)

        # change the font of the textedit
        self.textEdit.setFont(self.display_font)
        # max size of the textedit
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 450))


        # read context from the database
        self.db = Database('sentences.json')

        self.contexts = self.db.contexts()


        for i,j in enumerate(self.db.sentences(self.contexts[0])):
            b1 = self.button_initialiser(j)
            b1.clicked.connect(lambda state, b1=b1: self.textEdit.append(b1.text()))
            y = i % 3
            x = math.floor(i/3)
            self.gridLayout1.addWidget(b1,x,y)



        for i,j in enumerate(self.contexts):
            b1 = self.button_initialiser(j)
            b1.clicked.connect(lambda state, b1=b1: self.layout_button_initialiser(b1.text()))
            b1.setMaximumWidth(400)
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout2.addWidget(b1,x,y)
            # background color of the buttom
            # b1.setStyleSheet("background-color: rgb(0, 60, 120);")

        for i in range(4):
            b1 = QPushButton("Custom")
            b1.setFont(self.text_font)
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # max width of the button
            b1.setMaximumWidth(400)

            y = i % 2
            x = math.floor(i/2)
            self.gridLayout3.addWidget(b1,x,y)
            # background color of the buttom
            # b1.setStyleSheet("background-color: rgb(120, 60, 0);")

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

        def play_sound():
            # save text in new variable
            text = self.textEdit.toPlainText()
            # disable play press
            self.Setting1.setEnabled(False)
            # self.textEdit.clear()
            self.mytts.say(text)

            # enable play press
            self.Setting1.setEnabled(True)
        
        def erase():
            self.textEdit.clear()
            # self.initiate_custom_buttons()



        # when setting1 is clicked play the content of textedit
        self.Setting1.clicked.connect(lambda state, self=self: play_sound())

        # when setting3 is clicked clear the textedit
        self.Setting3.clicked.connect(lambda state, self=self: erase())


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


    def initiate_custom_buttons(self):
            # erase content of the gridlayout1
            for i in reversed(range(self.gridLayout1.count())):
                self.gridLayout1.itemAt(i).widget().setParent(None)
            # read the database

    def button_initialiser(self,text):
        b = MyButton(text)
        b.setFont(self.text_font)
        # make the buttom expand
        b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        b.rightclick.connect(lambda b=b: self.create_qinputdialog(b))
        # create Qinputdialog
        # text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        return b

    def layout_button_initialiser(self,context):
            for i,j in enumerate(self.db.sentences(context)):
                b1 = self.button_initialiser(j)
                b1.clicked.connect(lambda state, b1=b1: self.textEdit.append(b1.text()))
                y = i % 3
                x = math.floor(i/3)
                self.gridLayout1.addWidget(b1,x,y)

    def create_qinputdialog(self,button):
        text, ok = QInputDialog.getText(self, 'Text Saver', 'Enter text:', QLineEdit.Normal, button.text())
        if ok:
            # set botton text
            button.setText(text)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



# convert gui.ui to .py
# pyuic5 gui.ui -o gui.py
