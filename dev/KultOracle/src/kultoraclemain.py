from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow
from PyQt5.QtSql import QSqlDatabase
from PyQt5.Qt import QMessageBox
from PyQt5.QtCore import QTemporaryDir, QFile


def createConnection():


    #QDir::mkpath("../student");    
    #QFile::copy(":/data/kcdata", "")

    tmpDir=QTemporaryDir()
    #print("temporary dir:", tmpDir.path())
    
    fcFileCopy=QFile()
    fcFileCopy.copy(":/data/kcdata", tmpDir.path() + '/kcdata')
    
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setConnectOptions("QSQLITE_OPEN_READONLY")

    con.setDatabaseName(tmpDir.path() + '/kcdata')

    if not con.open():

        QMessageBox.critical(

            None,

            "KultOracle - Error!",

            "Database Error: %s" % con.lastError().databaseText(),

        )

        return False

    return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if not createConnection():
    
        sys.exit(1)
    
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

