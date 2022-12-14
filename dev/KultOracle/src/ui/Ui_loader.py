# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/loader.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoaderWindow(object):
    def setupUi(self, LoaderWindow):
        LoaderWindow.setObjectName("LoaderWindow")
        LoaderWindow.resize(588, 92)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoaderWindow.sizePolicy().hasHeightForWidth())
        LoaderWindow.setSizePolicy(sizePolicy)
        LoaderWindow.setMinimumSize(QtCore.QSize(588, 90))
        LoaderWindow.setMaximumSize(QtCore.QSize(588, 92))
        LoaderWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        LoaderWindow.setStyleSheet("background-color: rgb(60, 0, 0);\n"
"font: oblique 12pt \"DejaVu Sans\";")
        self.centralwidget = QtWidgets.QWidget(LoaderWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frmcontainer = QtWidgets.QFrame(self.centralwidget)
        self.frmcontainer.setFrameShape(QtWidgets.QFrame.Panel)
        self.frmcontainer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frmcontainer.setLineWidth(2)
        self.frmcontainer.setObjectName("frmcontainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frmcontainer)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(-1, 5, -1, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pbPdfLoader = QtWidgets.QProgressBar(self.frmcontainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbPdfLoader.sizePolicy().hasHeightForWidth())
        self.pbPdfLoader.setSizePolicy(sizePolicy)
        self.pbPdfLoader.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Great Vibes")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pbPdfLoader.setFont(font)
        self.pbPdfLoader.setStyleSheet("QProgressBar {\n"
"font: 18pt \"Great Vibes\";\n"
"text-align: center;\n"
"border: 1px solid black;\n"
"color: white;\n"
"background-color: rgb(200, 0, 0);\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(100, 0, 0);\n"
"min-height: 10px;\n"
"max-height: 10px;\n"
"width: 10px;\n"
"border-radius: 5px;\n"
"}")
        self.pbPdfLoader.setProperty("value", 24)
        self.pbPdfLoader.setAlignment(QtCore.Qt.AlignCenter)
        self.pbPdfLoader.setObjectName("pbPdfLoader")
        self.verticalLayout.addWidget(self.pbPdfLoader)
        self.lblStatus = QtWidgets.QLabel(self.frmcontainer)
        self.lblStatus.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Great Vibes")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblStatus.setFont(font)
        self.lblStatus.setStyleSheet("QLabel{\n"
"    font: 12pt \"Great Vibes\";\n"
"text-align: center;\n"
"border: 1px rgb(33, 0, 0);\n"
"color: white;\n"
"}")
        self.lblStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.lblStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblStatus.setObjectName("lblStatus")
        self.verticalLayout.addWidget(self.lblStatus)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frmcontainer, 0, 0, 1, 1)
        LoaderWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoaderWindow)
        QtCore.QMetaObject.connectSlotsByName(LoaderWindow)

    def retranslateUi(self, LoaderWindow):
        _translate = QtCore.QCoreApplication.translate
        LoaderWindow.setWindowTitle(_translate("LoaderWindow", "resource loader"))
        self.lblStatus.setText(_translate("LoaderWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoaderWindow = QtWidgets.QMainWindow()
    ui = Ui_LoaderWindow()
    ui.setupUi(LoaderWindow)
    LoaderWindow.show()
    sys.exit(app.exec_())
