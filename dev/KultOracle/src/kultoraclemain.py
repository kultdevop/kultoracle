from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow
from sqlscripts import database_ops



if __name__ == "__main__":
    import sys
    
    if not database_ops.initialiseDatabase():
    
        sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())

