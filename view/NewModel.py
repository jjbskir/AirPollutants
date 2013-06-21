from PyQt4 import QtCore, QtGui
import itertools

'''
Widget for creating a new air pollution model.
'''
class NewModel(QtGui.QWidget):
    
    # container to emit signals to other classes.
    procDone = QtCore.pyqtSignal(dict)
    
    '''
    Add input forms to page
    '''
    def __init__(self, parent=None):
        super(NewModel, self).__init__(parent)
        self.rowCount = 0
        self.createForm()
        self.addLayout()
    
    '''
    Create forms to be used to create a new model.
    ###########################################
    #    ATTENTION                            #
    # Variable names are very                 #
    # importnat for creating the run_codes    #
    # to create a new model scenario.         #
    ###########################################
    variable names:
    le          - line editing.
    btn         - button
    lbl         - label
    cb          - combo button.
    cb<><>      - feed stock.
    cb<><>_<><> - feed stock and activity.
    ''' 
    def createForm(self):
        self.lblS = QtGui.QLabel('Create A New Model', self)
        self.title = QtGui.QLabel('title: ')
        self.leTitle = QtGui.QLineEdit()
        # crops. and run codes.
        self.run_codes = QtGui.QLabel('run codes: ')
        self.cbSG = QtGui.QCheckBox('Switch Grass', self)
        self.cbSG.clicked.connect(self.showMore)
        self.cbFR = QtGui.QCheckBox('Forest Residue', self)
        self.cbCS = QtGui.QCheckBox('Corn Stover', self)
        self.cbCS.clicked.connect(self.showMore)
        self.cbWS = QtGui.QCheckBox('Wheat Straw', self)
        self.cbWS.clicked.connect(self.showMore)
        self.cbCG = QtGui.QCheckBox('Corn Grain', self)
        self.cbCG.clicked.connect(self.showMore)
        self.selectAll = QtGui.QCheckBox('Check All', self)
        self.selectAll.clicked.connect(self.showAll)
        # harvest methods.
        self.harvestMethods = QtGui.QLabel('Harvest Methods: ')
        # for switch grass and corn grain.
        self.cbSG_H1 = QtGui.QCheckBox('Harvest', self)
        self.cbSG_N1 = QtGui.QCheckBox('Non Harvest', self)
        self.cbSG_T1 = QtGui.QCheckBox('Transportation', self)
        self.cbSG_fsg = QtGui.QCheckBox('Fertilizer', self)
        self.cbSG_psg = QtGui.QCheckBox('Pesticide', self)
        # for corn stover.
        self.cbCS_RT = QtGui.QCheckBox('Reduce Till', self)
        self.cbCS_NT = QtGui.QCheckBox('No Till', self)
        self.cbCS_fcs = QtGui.QCheckBox('Fertilizer', self)
        # for wheat straw.
        self.cbWS_RT = QtGui.QCheckBox('Reduce Till', self)
        self.cbWS_NT = QtGui.QCheckBox('No Till', self)
        self.cbWS_fws = QtGui.QCheckBox('Fertilizer', self)
        # for corn grain. and Irrigation 
        # harvest.
        self.cbCG_CH = QtGui.QCheckBox('Harv Conv Till', self)
        self.cbCG_RH = QtGui.QCheckBox('Harv Reduced Till', self)
        self.cbCG_NH = QtGui.QCheckBox('Harv No Till', self)
        self.cbCG_fcg = QtGui.QCheckBox('Fertilizer', self)
        self.cbCG_pcg = QtGui.QCheckBox('Pesticide', self)
        # non-harvest
        self.cbCG_CN = QtGui.QCheckBox('Non Harv Conv Till', self)
        self.cbCG_RN = QtGui.QCheckBox('Non Harv Reduced Till', self)
        self.cbCG_NN = QtGui.QCheckBox('Non Harv No Till', self)
        # irrigation
        self.cbCG_ID = QtGui.QCheckBox('Diesel Irrigation', self)
        self.cbCG_IL = QtGui.QCheckBox('LPG Irrigation', self)
        self.cbCG_IC = QtGui.QCheckBox('CNG Irrigation', self)
        self.cbCG_IG = QtGui.QCheckBox('Gasoline Irrigation', self)
        # Fertilizer distribution.
        # aa, an, as, ur, ns
        # labels. annhydrous_amonia, ammonium_nitrate, ammonium_sulfate, urea, nsol
        self.lblFert = QtGui.QLabel('Fertilizer Distribution. Leave blank for default values.', self)
        self.fertaa = QtGui.QLabel('annhydrous_amonia', self)
        self.fertan = QtGui.QLabel('ammonium_nitrate', self)
        self.fertas = QtGui.QLabel('ammonium_sulfate', self)
        self.fertur = QtGui.QLabel('urea', self)
        self.fertns = QtGui.QLabel('nsol', self)
        # line edits.
        self.leFeaa = QtGui.QLineEdit()
        self.leFean = QtGui.QLineEdit()
        self.leFeas = QtGui.QLineEdit()
        self.leFeur = QtGui.QLineEdit()
        self.leFens = QtGui.QLineEdit()
        # add button to create model.
        self.btnCreate = QtGui.QPushButton("Create Model", self)
        self.btnCreate.clicked.connect(self.on_button_clicked)
    
    '''
    Add buttons and labels to the layout.
    '''
    def addLayout(self):
        # layout
        layout = QtGui.QGridLayout()
        #layout.addWidget(self., 0, 1)
        self.addRow(layout, 'lblS')
        # add title to program.
        layout.addWidget(self.title, 1, 0)
        layout.addWidget(self.leTitle, 1, 1)
        # run code and harvest method hearders.
        layout.addWidget(self.run_codes, 2, 0)
        layout.addWidget(self.harvestMethods, 2, 1)
        layout.addWidget(self.selectAll, 2, 2)
        # add switch grass.
        self.addRow(layout, 'cbSG', 3)
        # add forest redidue.
        self.addRow(layout, 'cbFR')
        # add corn stover.
        self.addRow(layout, 'cbCS')
        # add wheat straw.
        self.addRow(layout, 'cbWS')
        # add corn grain.
        self.addRow(layout, 'cbCG')
        # fertilizer buttons.
        self.addRow(layout, 'lblFert')
        self.addRow(layout, 'fert')
        self.addRow(layout, 'leFe')
        # add submit button.
        self.addRow(layout, 'btnCreate')
        #layout.addWidget(self.btnCreate, 12, 1)
        # close all of the nested activity check boxes.
        self.showMore()
        self.setLayout(layout)
    
    '''
    Add rows to the layout.
    @param layout: Layout to add widget to.
    @param attribute: Name of variable to look for.
    @param row: Used when a row was added without the help of addRow(). 
    Increases the row count to it's value. (int) 
    '''
    def addRow(self, layout, attribute, row=False):
        # change row count.
        if row:
            self.rowCount = row
        widgets = self.getAllAtributes(attribute)
        col = 0
        # add all widgets with attribute to the row.
        for widget in widgets:
            if col == 5:
                col = 1
                self.rowCount += 1
            variable = widget[1]
            layout.addWidget(variable, self.rowCount, col)
            col += 1
        self.rowCount += 1
        
    '''
    Get all of the inputs that are used to create a new model.
    '''
    def getInputs(self, boxes, title, fertilizers):
        inputs = {}
        inputs['checkBoxes'] = boxes
        inputs['title'] = title
        inputs['fertilizers'] = fertilizers
        return inputs
    
    '''
    Get all variables that start with a specific attribute.
    @param attribute: variable's name to look for.
    @return: A kust containing sets. The sets are a pair containing the variable's name and the variable itself. 
    '''
    def getAllAtributes(self, attribute):
        classAttributes = dir(self)
        variables = []
        for attr in classAttributes:
            if attr.startswith(attribute):
                le = getattr(self, attr)
                variables.append((attr, le))
        return variables
    
    '''
    Get all the check boxed buttons variable names and weather they have been clicked.
    @return: Dictionary mapping name of button variable to it's state.
    '''
    def getBoxes(self):
        # get all attributes from the class.
        return self.getAllAtributes('cb')
    
    '''
    Get all of the fertilizer attributes.
    aa, an, as, ur, ns
    @return: List containing all of the fertilizer contributions.  
    ''' 
    def getFert(self):
        fertsVars = self.getAllAtributes('leFe')
        return fertsVars
            
                
    '''
    Sends the searched schema and table to the controller.
    The controller then Create a new Table model and sends it to the Table view.
    @param schema: Schema to look up in db.
    @param table: Table to look up in db. 
    @return: text from the two line edit slots. 
    @QtCore.pyqtSlot(): Send signals to other classes.
    '''
    def on_button_clicked(self):
        inputs = self.getInputs(self.getBoxes(), self.leTitle.text(), self.getFert())
        self.procDone.emit(inputs)
        
    '''
    Once a feed stock has been clicked, let the view see the activities for
    harvest that are associated with the feed stock.
    '''
    def showMore(self):
        checkBoxes = self.getBoxes()
        feedStock = 'Empty'
        btnState = 0
        for box in checkBoxes:
            name = box[0]
            var = box[1]
            # if the feed stock box is clicked, then go into this part.
            # relies on the fact that the list of checkBoxes is alphebetically ordered.
            # if the activity is clicked then show it. Else do not show the box.
            if feedStock in name:
                if btnState == 0: var.close()
                else: var.show()
            # if the button is a feed stock then set states.
            elif len(name) == 4:
                feedStock = name[-2:]
                if var.checkState() == 2: btnState = 2
                else: btnState = 0

    def showAll(self):
        checkBoxes = self.getBoxes()
        showAll = self.selectAll.checkState()
        for box in checkBoxes:
            var = box[1]
            if showAll == 2:
                var.setCheckState(2)
            elif showAll == 0:
                var.setCheckState(0)
        self.showMore()

                    
                
                
                
            
            