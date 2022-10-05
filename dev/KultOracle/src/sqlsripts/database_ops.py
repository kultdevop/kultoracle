from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.Qt import QMessageBox, QIODevice, QTextStream
from PyQt5.QtCore import QTemporaryDir, QFile


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
    return runDDLScripts("./sqlsripts/DDL.sql")
    


def runDDLScripts(fullpathscriptfilename):
    query = QSqlQuery()
    scriptFile = QFile(fullpathscriptfilename)
    
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
    
