from PyQt4 import QtGui, QtCore
from view.Table import Table
from view.Search import Search
from view.NewModel import NewModel
from src.Inputs import Inputs
from src.Validation import Validation
from src.AirPollution.Driver import Driver

'''
Main window of the program.
Controlls internal flow of program.
All the views when needing to communicate with other views or 
the model must pass through this class.
The Controller then grabs needed data from the model and will
create any new views that are needed.
'''
class Controller(QtGui.QMainWindow):
    
    '''
    Create the starting window.
    @param model: data from the db nicely ordered.
    '''
    def __init__(self, model):
        QtGui.QMainWindow.__init__(self)
        # model, holds data.
        self.model = model
        # used to validate user inputs.
        self.validate = Validation()
        # main view.
        self.setGeometry(300, 300, 500, 380)
        self.setWindowTitle('Air Quality Model')
        # smaller search bar.  
        self.search = Search(self.model.schemas)
        # connect search bar widget to the controler. The controller connects the search bar to the Table of data.
        self.search.procDone.connect(self._widgetSearch)
        # connection to show the table search.
        self.search.procTable.connect(self._getTables)
        # menu bar.
        self.addMenuBar()


    '''
    Add menu bar to program.
    '''
    def addMenuBar(self):
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
    
    '''
    Used in the Search view. Once a schema has been selected,
    then allow the user to select a table to pick data from.
    @param schema: Schema in the db corresponding to a run title.
    '''  
    def _getTables(self, schema):
        tables = self.model.getTables(schema)
        self.search.addTable(tables)
        
    '''
    Set the central widget to the NewModel widget to create a new model
    scenario.
    '''    
    def _newModel(self):
        # create new model.
        self.newModel = NewModel()
        # connect the new model to the controller.
        self.newModel.procDone.connect(self._runNewModel)
        # set new model screen to main widget.
        self.setCentralWidget(self.newModel)
        # close ferts.
        self.newModel.closeAllFerts()
        # add status bar.
        self.statusBar().showMessage('Ready to Run New Model')
    
    '''
    Run a new model.
    @param inputs: Inputs from the NewModel view. 
    A dictionary with various values such as title and run codes. dict(string, list)
    '''
    def _runNewModel(self, inputs):
        self.statusBar().showMessage('Starting New Model')  
        inputs = Inputs(inputs)
        # only used for validation purposes. Are boolean.
        self.validate.title(inputs.title)
        self.validate.runCodes(inputs.run_codes)
        self.validate.fertDist(inputs.fertDist)
        self.validate.ferts(inputs.ferts)
        self.validate.pest(inputs.pestFeed)
        
        print inputs.fertDist
        print inputs.alloc
        print ''
        print inputs.run_codes
        print inputs.ferts
        print inputs.pestFeed
        print ''
        print inputs.operations
        
        # make sure all of the variables to run the model have been created.
        if not self.validate.errors:
            self.statusBar().showMessage('Initiating Air Model.')    
            # get db and add schema
            db = self.model.db
            db.schema = inputs.title
            # create the subprocess module that will run NONROAD in the background.
            self.qprocess = QtCore.QProcess(self)
            # send signal when subprocess has started.
            self.qprocess.started.connect(self._processStart)
            # when the subprocess is finished, it will send a signal to the controller to finish running the air model.
            self.qprocess.finished.connect(self._processSave)
            # read any new data.
            self.qprocess.readyReadStandardOutput.connect(self._processStatus) 
            # send signal if a error has occured.
            self.qprocess.error.connect(self._processError)
            # create air model.
            self.airModel = Driver(inputs.title, inputs.run_codes, db)
            #self.airModel.setupNONROAD()
            # create progress bar before running NONROAD model, to keep track of progress.
            self.timer = 0
            #create a global fertilizer to pass to the model.
            self.fertDist = inputs.fertDist
            # weather each feed stock should calculate emmisions from fertilizers.
            self.ferts = inputs.ferts
            # weather some feedstocks should calculate emmisions from pesticides.
            self.pestFeed = inputs.pestFeed
            # which operations to use for run.
            self.operations = inputs.operations
            self.alloc = inputs.alloc
            # grab the total number of files that need to be ran.
            batchFiles = self.airModel.batch.getBatchFiles()
            self.bar = QtGui.QProgressBar()
            self.bar.setRange(self.timer, batchFiles)
            self.bar.setValue(self.timer)
            self.bar.setWindowTitle("NONROAD Progress")
            self.bar.show()
            # run NONROAD.
            #self.airModel.runNONROAD(self.qprocess)
            
            self.airModel.saveData(self.ferts, self.fertDist, self.pestFeed, self.operations, self.alloc)
            
        # if not able to validate inputs. 
        else:
            self.statusBar().showMessage('ERROR: could not run model')  
            # output errors in pop up boxes.
            for error in self.validate.getErrors():
                QtGui.QMessageBox.about(self, "Validation", error)
            
    '''
    Check if qprocess has began running the NONROAD model.
    @param qprocess: QtCore.QProcess, runs subprocess. Emits signal.
    '''    
    def _processStart(self):
        self.statusBar().showMessage('Running NONROAD')
    
    '''
    Uses a progress bar to update the user on how far the NONROAD model has ran.
    Works by seeing how many files the NONROAD model has to process and making this te range for the bar.
    The subprocess reads data from the NONROAD output, and detects when it has completed a file.
    Every time this occurs a timer is updated, and the bar increase in percentage.
    '''
    def _processStatus(self):
        # get the current data from the subprocess.
        output = self.qprocess.readAllStandardOutput()
        # check to see if a file has been finished processing.
        if 'Successful completion' in output:
            self.timer += 1
            # Increase progress bar value.
            self.bar.setValue(self.timer)
        
    '''
    Save the data from the air model, once the subprocess is finished.
    Slot connecting Air model to the Controller.
    @param qprocess: QtCore.QProcess, runs subprocess. Emits signal.
    '''  
    def _processSave(self):
        self.bar.close()
        self.statusBar().showMessage('Finished Running NONROAD')
        self.airModel.saveData(self.fertDist)
        self._newModel()
    
    '''
    Tell the user if qprocess detects a error when running NONROAD.
    @param qprocess: QtCore.QProcess, runs subprocess. Emits signal.
    '''
    def _processError(self):
        self.statusBar().showMessage('ERROR: while running NONROAD')
        
    '''
    Show the search bar to look through the data.
    '''   
    def _viewModel(self):
        self.search.show()
         
