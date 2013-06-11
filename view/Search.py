from PyQt4 import QtCore, QtGui

'''
Search bar for looking up data in the db.
'''
class Search(QtGui.QWidget):
    
    # container to emit signals to other classes.
    procDone = QtCore.pyqtSignal(tuple)
    
    '''
    Add search bar and buttons to layout.
    '''
    def __init__(self, schemas, tables, parent=None):
        super(Search, self).__init__(parent)
        
        # create scroll options for schema and table
        lblS = QtGui.QLabel('Schema', self)
        self.schema = QtGui.QComboBox(self)
        for schema in schemas:
            self.schema.addItem(schema)
        
        lblT = QtGui.QLabel('Table', self)
        self.table = QtGui.QComboBox(self)
        for table in tables:
            self.table.addItem(table)

        # Create button
        self.btnSearch = QtGui.QPushButton("Search", self)
        self.btnSearch.clicked.connect(self.on_button_clicked)
        # add view to the layout.
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(lblS)
        self.layout.addWidget(self.schema)
        self.layout.addWidget(lblT)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btnSearch)
        self.setGeometry(300, 170, 400, 100)
        self.setWindowTitle('Search Database')
        # show widget on the screen.
        self.show()

    '''
    Sends the searched schema and table to the controller.
    The controller then Create a new Table model and sends it to the Table view.
    @param schema: Schema to look up in db.
    @param table: Table to look up in db. 
    @return: text from the two line edit slots. 
    @QtCore.pyqtSlot(): Send signals to other classes.
    '''
    def on_button_clicked(self):
        self.procDone.emit((self.schema.currentText(), self.table.currentText()))
        #self.procDone.emit(QtCore.SIGNAL("signalIntList"), self.schema.text(), self.table.text())
        #self.QtCore.QObject.emit(QtCore.SIGNAL("signalIntList"), self.schema.text(), self.table.text())





