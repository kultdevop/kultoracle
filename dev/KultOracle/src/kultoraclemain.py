from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow
from sqlsripts import database_ops



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if not database_ops.initialiseDatabase():
    
        sys.exit(1)
    
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

