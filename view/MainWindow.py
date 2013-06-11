import sys
from PyQt4 import QtGui, QtCore
from Table import Table
from Search import Search
from NewModel import NewModel

'''
Main window of the program.
'''
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, model):
        QtGui.QMainWindow.__init__(self)
        # model, holds data.
        self.model = model
        # main view.
        self.setGeometry(300, 300, 500, 380)
        self.setWindowTitle('Air Quality Model')
        # smaller search bar.  
        self.search = Search(self.model.schemas, self.model.getTables(self.model.schemas[0]))
        # connect search bar widget to the controler. The controller connects the search bar to the Table of data.
        self.search.procDone.connect(self._widgetSearch)
        # exit program action
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        # create new model action.
        modelAction = QtGui.QAction('New Model', self)
        modelAction.setStatusTip('New model')
        modelAction.triggered.connect(self._newModel)
        # View a old model action.
        viewAction = QtGui.QAction('View Model', self)
        viewAction.setStatusTip('View model')
        viewAction.triggered.connect(self._viewModel)
        # add a menu bar.
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(modelAction)
        fileMenu.addAction(viewAction)

        
                
    '''
    Receives signals from Search object. Creates a new table from it.
    @param schema: Message from Search. Name of the schema to create data model from.
    @return: Table view that is made into the central widget.
    @QtCore.pyqtSlot(str): Slot for receiving message.   
    '''
    def _widgetSearch(self, data):
        # convert to lower case b/c all of the db is saved as lower case.
        schema = str(data[0]).lower()
        table = str(data[1]).lower()
        # create a data model from the db. summedemissions
        self.model.newModel(schema, table) 

            
        # Create a new table view.
        self.table = Table(self.model.model, self.model.header, self)
        # add text to top of table.
        self.table.leSchema.setText(schema)
        self.table.leTable.setText(table)
        # make table the central widget.
        self.setCentralWidget(self.table)
        # raise any errors.
        self.raise_()
        
    def _newModel(self):
        self.newModel = NewModel()
        self.setCentralWidget(self.newModel)
        
        
    def _viewModel(self):
        self.search.show()
         
        
if __name__ == '__main__':
    arraydata = [['00','01','02'],
                ['10','11','12'],
                ['20','21','22']]
    headers = ['gas1', 'gas2', 'gas3']
    app = QtGui.QApplication(sys.argv)
    myApp = MainWindow(arraydata, headers)
    sys.exit(app.exec_())