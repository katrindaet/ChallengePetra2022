import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QPushButton
)
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
            self.gridLayout.addWidget(b1,x,y)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())