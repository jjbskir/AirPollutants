'''
Main source code. Where the program is run.
'''

from Database import Database
from model.Model import Model
from view.MainWindow import MainWindow
import sys
from PyQt4 import QtGui, QtCore
   
if __name__ == "__main__": 
    
    db = Database('allfeed')
    m = Model(db)
    
    app = QtGui.QApplication(sys.argv)
    myController = MainWindow(m)
    myController.show()
    sys.exit(app.exec_()) 
    
