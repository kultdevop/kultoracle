from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.Qt import QMessageBox, QIODevice, QTextStream
from PyQt5.QtCore import QTemporaryDir, QFile
import os
import sys


def initialiseDatabase():

    #tmpDir=QTemporaryDir()
    dbfile = QFile('./kcdata')
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setConnectOptions("QSQLITE_OPEN_READWRITE")
    if dbfile.exists():
        dbfile.remove()
    
    con.setDatabaseName(dbfile.fileName())

    if not con.open():
        QMessageBox.critical(
            None,
            "KultOracle - Error!",
            "Database Error: %s" % con.lastError().databaseText()
        )
        return False
    return runDDLScripts("DDL.sql")
    


def runDDLScripts(fullpathscriptfilename):
    query = QSqlQuery()
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_script = os.path.abspath(os.path.join(bundle_dir, fullpathscriptfilename))

    
    scriptFile = QFile(path_to_script)
    
    if scriptFile.open(QIODevice.ReadOnly):
        # The SQLite driver executes only a single (the first) query in the QSqlQuery
        #  if the script contains more queries, it needs to be splitted.
        scriptQueries = QTextStream(scriptFile).readAll().split(';')
    
        for queryTxt in scriptQueries:
            if not str(queryTxt).strip():
                continue            
            if not query.exec(queryTxt):
                QMessageBox.critical(
                    None,
                    "KultOracle - Error!",
                    "Database Error: %s" % query.lastError().databaseText()
                )
                return False
            query.finish()
    else:
        QMessageBox.critical(
                    None,
                    "KultOracle - Error!",
                    "Cannot find file: %s" % fullpathscriptfilename
                )
        return False
    
    return True
    
