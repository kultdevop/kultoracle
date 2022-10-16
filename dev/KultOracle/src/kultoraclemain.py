from PyQt5 import QtWidgets, QtGui
from ui.mainwindow import MainWindow
from sqlscripts import database_ops



if __name__ == "__main__":
    import sys
    
    if not database_ops.initialiseDatabase():
        sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    _id = QtGui.QFontDatabase.addApplicationFont("greatvibes-regular")
    print(QtGui.QFontDatabase.applicationFontFamilies(_id))
    ui = MainWindow()
    sys.exit(app.exec_())

