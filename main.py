import os
import sys
import math

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from auto_complete import auto_complete

from GUI import Ui_MainWindow
from Settings import Ui_Dialog
import tts
from database import Database

class MyTextEdit(QTextEdit):
    enterPressed = pyqtSignal()

    def __init__(self,  *args, **kwargs):
        super(MyTextEdit, self).__init__(*args, **kwargs)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return or e.key() == Qt.Key_Escape:
            self.enterPressed.emit()
        else:
            super().keyPressEvent(e)

class MyButton(QPushButton):
    textChanged = pyqtSignal(str, str)

    def __init__(self, text):
        super().__init__()

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.resize(self.size())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFocusPolicy(Qt.NoFocus)

        self.edit = MyTextEdit(self)
        self.edit.resize(self.size())
        self.edit.setAlignment(Qt.AlignCenter)
        self.edit.viewport().setAutoFillBackground(False)
        self.edit.enterPressed.connect(lambda self=self: self.save())

        self.edit.setText(text)
        self.switchToViewMode()

    def switchToEditMode(self):
        self.edit.setText(self.label.text())
        self.label.hide()
        self.edit.show()
        self.setFocusProxy(self.edit)

    def switchToViewMode(self):
        self.label.setText(self.edit.toPlainText())
        self.label.show()
        self.edit.hide()
        self.setFocusProxy(None)
        
    def resizeEvent(self, event):
        self.label.resize(self.size())
        self.edit.resize(self.size())

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            self.switchToEditMode()
        else:
            super().mousePressEvent(QMouseEvent)

    def text(self):
        return self.label.text()

    def setText(self, text):
        self.label.setText(text)

    def save(self):
        self.textChanged.emit(self.label.text(), self.edit.toPlainText())
        self.switchToViewMode()

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.savedSettings = QSettings("SuperPetra2022")

        # Text to speech shortcut
        keySequence = QKeySequence('Ctrl+P')
        self.enter_shortcut = QShortcut(keySequence, self)
        self.enter_shortcut.activated.connect(self.play_sound)

        # UI setup
        self.setupUi(self)
        self.mytts = tts.TTS()
        if self.savedSettings.value('voiceRate') is not None:
            self.mytts.setRate(float(self.savedSettings.value('voiceRate', 1.0)))
        if self.savedSettings.value('voiceId') is not None:
            self.mytts.setVoice(self.savedSettings.value('voiceId'))
        self.display_font = QFont("Arial", 24)
        # set font color
        self.display_font.setBold(True)


        # change the font of the textedit
        self.textEdit.setFont(self.display_font)
        # max size of the textedit
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 450))

        # read context from the database
        self.db = Database('sentences.json')

        self.language = self.savedSettings.value('language', 'Deutsch')



        # Load Autocomplete
        self.load_autocomplete()

        self.current_context = self.db.contexts()[0]
        self.initiate_custom_buttons()
        self.layout_button_initialiser(self.current_context)

        # add icons in settings
        self.Setting2.setIcon(QIcon(os.path.join('icons_gui', 'play.svg')))
        self.Setting2.setIconSize(self.Setting2.size())

        self.Setting3.setIcon(QIcon(os.path.join('icons_gui', 'delete.svg')))
        self.Setting3.setIconSize(self.Setting3.size())

        self.Setting4.setIcon(QIcon(os.path.join('icons_gui', 'context.png')))
        self.Setting4.setIconSize(self.Setting4.size())

        self.Setting5.setIcon(QIcon(os.path.join('icons_gui', 'plus.svg')))
        self.Setting5.setIconSize(self.Setting5.size())

        self.Setting6.setIcon(QIcon(os.path.join('icons_gui', 'settings.png')))
        self.Setting6.setIconSize(self.Setting6.size())

        self.Setting1.setIcon(QIcon(os.path.join('icons_gui', 'copy.svg')))
        self.Setting1.setIconSize(self.Setting1.size())
        self.Setting1.clicked.connect(lambda state, self=self: QGuiApplication.clipboard().setText(self.textEdit.toPlainText()))
        
        def erase():
            self.textEdit.clear()
            # self.initiate_custom_buttons()


        # when setting1 is clicked play the content of textedit
        self.Setting2.clicked.connect(lambda state, self=self: self.play_sound())

        # when setting3 is clicked clear the textedit
        self.Setting3.clicked.connect(lambda state, self=self: erase())

        # when setting6 is clicked clear the textedit
        self.Setting6.clicked.connect(lambda state, self=self: self.open_settings())

        # when setting4 is clicked create new context
        self.Setting4.clicked.connect(lambda state, self=self: self.add_new_context())

        # when setting5 is clicked create new sentence
        self.Setting5.clicked.connect(lambda state, self=self: self.add_new_sentence())

        # when cursor changes position in text
        self.textEdit.cursorPositionChanged.connect(lambda: self.take_word_text_edit())

        # > mytts = tts.TTS()
        # > mytts.say('Hello, World')
        # loop through Setting1 to 6 and make the button expand
        for i in range(6):
            b1 = getattr(self, "Setting" + str(i+1))
            b1.setIconSize(QSize(200,200))
            # set minimum size of the button
            b1.setMinimumSize(QSize(100,100))
            b1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

            b1.setMaximumWidth(300)


        # adapt size of icon
        self.Setting2.setIconSize(QtCore.QSize(100, 100))

    def load_autocomplete(self):

        autocomplete_file = {
            'Deutsch': 'german_dataset_auto_complete.json',
            'English': 'english_dataset_auto_complete.json',
        }.get(self.language, 'german_dataset_auto_complete.json')

        self.auto_complete = auto_complete(autocomplete_file)

    def resizeEvent(self, event):
        self.Setting2.setIconSize(self.Setting2.size())
        self.Setting3.setIconSize(self.Setting3.size())
        self.Setting4.setIconSize(self.Setting4.size())
        self.Setting5.setIconSize(self.Setting5.size())
        self.Setting6.setIconSize(self.Setting6.size())
        self.Setting1.setIconSize(self.Setting1.size())

    def initiate_custom_buttons(self):
        # erase content of the gridlayout1
        for i in reversed(range(self.gridLayout2.count())):
            self.gridLayout2.itemAt(i).widget().setParent(None)
        # read the database
        for i,j in enumerate(self.db.contexts()):
            b1 = self.button_initialiser(j)
            b1.clicked.connect(lambda state, b1=b1: self.layout_button_initialiser(b1.text()))
            b1.textChanged.connect(lambda oldtext, newtext: self.db.replace_context(oldtext, newtext))
            b1.setMaximumWidth(400)
            y = i % 2
            x = math.floor(i/2)
            self.gridLayout2.addWidget(b1,x,y)
            # background color of the buttom
            # b1.setStyleSheet("background-color: rgb(0, 60, 120);")

    def initiate_auto_complete(self, predicted_words):
        for i in reversed(range(self.gridLayout1.count())):
            self.gridLayout1.itemAt(i).widget().setParent(None)
        for i,j in enumerate(predicted_words):
            b1 = self.button_initialiser(j)
            b1.clicked.connect(lambda state, b1=b1: self.add_predicted_word(b1.text()))
            if len(b1.text().split())==1: #if it is a word count for dictionary, if a sentence, pass
                b1.clicked.connect(lambda state, b1=b1: self.auto_complete.increment_count(b1.text()))

            b1.setMaximumWidth(400)
            y = i % 2
            x = math.floor(i / 2)
            self.gridLayout1.addWidget(b1, x, y)

    def add_predicted_word(self, word):
        text = self.textEdit.toPlainText()
        sentence = text.split()
        sentence.pop(-1)
        sentence =' '.join(sentence)
        self.textEdit.clear()
        self.textEdit.append(sentence+' '+word+' ')

    def take_word_text_edit(self):
        text = self.textEdit.toPlainText()
        try:
            if not text:
                self.layout_button_initialiser(self.current_context)
            elif text[-1] != ' ':
                words = text.split()
                word_prefix = words[-1]
                predicted_words = self.auto_complete.predict(word_prefix)
                predicted_sentences = self.db.sentences_containing(word_prefix)
                self.initiate_auto_complete(predicted_words + predicted_sentences)
            elif text[-1] == ' ':
                words = text.split()
                self.auto_complete.increment_count(words[-1])


        except:
            pass



    def button_initialiser(self,text):
        b = MyButton(text)
        # make the button expand
        b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # create Qinputdialog
        # text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        return b

    def layout_button_initialiser(self,context):
        for i in reversed(range(self.gridLayout1.count())):
            self.gridLayout1.itemAt(i).widget().setParent(None)
        self.current_context = context
        for i,j in enumerate(self.db.sentences(context)):
            b1 = self.button_initialiser(j)
            b1.clicked.connect(lambda state, b1=b1: self.textEdit.append(b1.text()))
            b1.textChanged.connect(lambda oldtext, newtext: self.db.replace_sentence(self.current_context, oldtext, newtext))
            y = i % 3
            x = math.floor(i/3)
            self.gridLayout1.addWidget(b1,x,y)

    def create_qinputdialog(self,button):
        text, ok = QInputDialog.getText(self, 'Text Saver', 'Enter text:', QLineEdit.Normal, button.text())
        if ok:
            # set button text
            old_text = button.text()
            button.setText(text)
            self.db.replace_sentence(self.current_context, old_text, button.text())
            # # find the old_text in self.db.sentences(self.context)
            # sentences = self.db.sentences(self.current_context)
            # for i,j in enumerate(sentences):
            #     if j == old_text:
            #         sentences[i] = button.text()
            #         self.db.replace_sentences(self.current_context, sentences)
            #         break

    def add_new_context(self):
        text, ok = QInputDialog.getText(self, 'Add new context', 'Enter text:')
        if ok:
            # add new context to database

            self.db.add_new_context(text)
            self.initiate_custom_buttons()

    def add_new_sentence(self):
         text, ok = QInputDialog.getText(self, 'Add new sentence', 'Enter text:')
         if ok:
             # add new context to database
             self.db.add_new_sentence(self.current_context, text)
             self.layout_button_initialiser(self.current_context)

    def play_sound(self):
        # save text in new variable
        text = self.textEdit.toPlainText()
        # disable play press
        self.Setting1.setEnabled(False)
        # self.textEdit.clear()
        self.mytts.say(text)

        # enable play press
        self.Setting1.setEnabled(True)

    def open_settings(self):
        # open the settings GUI
        self.settings = Settings(self.mytts, self)

        self.settings.show()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.auto_complete.save_json()

class Settings(QDialog, Ui_Dialog):
    def __init__(self, tts, app, parent=None):

        super().__init__(parent)

        self.tts = tts
        self.app = app
        self.setupUi(self)
        for voice_id, name in tts.voices().items():
            self.comboBox.addItem(name, voice_id)
        self.comboBox.setCurrentText(tts.voiceId())
        self.horizontalSlider.setValue(int(100 * tts.rate()))
        self.buttonBox.accepted.connect(lambda self=self: self.OK())

        self.comboBox_2.addItem('Deutsch')
        self.comboBox_2.addItem('English')
        self.comboBox_2.setCurrentText(app.language)




    def OK(self):
        self.tts.setRate(self.horizontalSlider.value() / 100)
        self.tts.setVoice(self.comboBox.currentData())
        newlanguage = self.comboBox_2.currentText()
        if newlanguage != self.app.language:
            self.app.language = newlanguage
            self.app.load_autocomplete()

        self.app.savedSettings.setValue('voiceId', self.comboBox.currentData())
        self.app.savedSettings.setValue('voiceRate', self.horizontalSlider.value() / 100)
        self.app.savedSettings.setValue('language', self.app.language)

        self.app.savedSettings.sync()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Arial", 24)
    font.setBold(True)
    app.setFont(font)
    win = Window()
    win.showMaximized()
    sys.exit(app.exec())

# convert gui.ui to .py
# pyuic5 gui.ui -o gui.py
