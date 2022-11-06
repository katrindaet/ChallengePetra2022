# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(519, 368)
        self.formLayout_2 = QtWidgets.QFormLayout(Dialog)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setMinimum(25)
        self.horizontalSlider.setMaximum(400)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.horizontalSlider)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Speed"))
        self.label.setText(_translate("Dialog", "Voice Selection"))
        self.label_3.setText(_translate("Dialog", "Language"))
