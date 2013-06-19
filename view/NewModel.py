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
        self.createForm()
    
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
    cb          - combo button.
    cb<><>      - feed stock.
    cb<><>_<><> - feed stock and activity.
    ''' 
    def createForm(self):
        lblS = QtGui.QLabel('Create A New Model', self)
        title = QtGui.QLabel('title: ')
        self.leTitle = QtGui.QLineEdit()
        # crops. and run codes.
        run_codes = QtGui.QLabel('run codes: ')
        self.cbSG = QtGui.QCheckBox('Switch Grass', self)
        self.cbSG.clicked.connect(self.showMore)
        self.cbFR = QtGui.QCheckBox('Forest Residue', self)
        self.cbCS = QtGui.QCheckBox('Corn Stover', self)
        self.cbCS.clicked.connect(self.showMore)
        self.cbWS = QtGui.QCheckBox('Wheat Straw', self)
        self.cbWS.clicked.connect(self.showMore)
        self.cbCG = QtGui.QCheckBox('Corn Grain', self)
        self.cbCG.clicked.connect(self.showMore)
        # harvest methods.
        harvestMethods = QtGui.QLabel('Harvest Methods: ')
        # for switch grass and corn grain.
        self.cbSG_H1 = QtGui.QCheckBox('Harvest', self)
        self.cbSG_N1 = QtGui.QCheckBox('Non Harvest', self)
        self.cbSG_T1 = QtGui.QCheckBox('Transportation', self)
        # for corn stover.
        self.cbCS_RT = QtGui.QCheckBox('Reduce Till', self)
        self.cbCS_NT = QtGui.QCheckBox('No Till', self)
        # for wheat straw.
        self.cbWS_RT = QtGui.QCheckBox('Reduce Till', self)
        self.cbWS_NT = QtGui.QCheckBox('No Till', self)
        # for corn grain. and Irrigation 
        # harvest.
        self.cbCG_CH = QtGui.QCheckBox('Harvest Conventional Till', self)
        self.cbCG_RH = QtGui.QCheckBox('Harvest Reduced Till', self)
        self.cbCG_NH = QtGui.QCheckBox('Harvest No Till', self)
        # non-harvest
        self.cbCG_CN = QtGui.QCheckBox('Non Harvest Conventional Till', self)
        self.cbCG_RN = QtGui.QCheckBox('Non Harvest Reduced Till', self)
        self.cbCG_NN = QtGui.QCheckBox('Non Harvest No Till', self)
        # irrigation
        self.cbCG_ID = QtGui.QCheckBox('Diesel Irrigation', self)
        self.cbCG_IL = QtGui.QCheckBox('LPG Irrigation', self)
        self.cbCG_IC = QtGui.QCheckBox('CNG Irrigation', self)
        self.cbCG_IG = QtGui.QCheckBox('Gasoline Irrigation', self)
        # add button to create model.
        self.btnCreate = QtGui.QPushButton("Create Model", self)
        self.btnCreate.clicked.connect(self.on_button_clicked)
        
        # layout
        layout = QtGui.QGridLayout()
        layout.addWidget(lblS, 0, 1)
        # add title to program.
        layout.addWidget(title, 2, 0)
        layout.addWidget(self.leTitle, 2, 1)
        # run code and harvest method hearders.
        layout.addWidget(run_codes, 3, 0)
        layout.addWidget(harvestMethods, 3, 1)
        # add switch grass.
        layout.addWidget(self.cbSG, 4, 0)
        layout.addWidget(self.cbSG_H1, 4, 1)
        layout.addWidget(self.cbSG_N1, 4, 2)
        layout.addWidget(self.cbSG_T1, 4, 3)
        # add forest redidue.
        layout.addWidget(self.cbFR, 5, 0)
        # add corn stover.
        layout.addWidget(self.cbCS, 6, 0)
        layout.addWidget(self.cbCS_RT, 6, 1)
        layout.addWidget(self.cbCS_NT, 6, 2)
        # add wheat straw.
        layout.addWidget(self.cbWS, 7, 0)
        layout.addWidget(self.cbWS_RT, 7, 1)
        layout.addWidget(self.cbWS_NT, 7, 2)
        # add corn grain.
        layout.addWidget(self.cbCG, 8, 0)
        layout.addWidget(self.cbCG_CH, 8, 1)
        layout.addWidget(self.cbCG_RH, 8, 2)
        layout.addWidget(self.cbCG_NH, 8, 3)
        
        layout.addWidget(self.cbCG_CN, 8, 4)
        layout.addWidget(self.cbCG_RN, 8, 5)
        layout.addWidget(self.cbCG_NN, 8, 6)
        
        layout.addWidget(self.cbCG_ID, 8, 7)
        layout.addWidget(self.cbCG_IL, 8, 8)
        layout.addWidget(self.cbCG_IC, 8, 9)
        layout.addWidget(self.cbCG_IG, 8, 10)
        layout.addWidget(self.btnCreate, 9, 1)
        # close all of the nested activity check boxes.
        self.showMore()
        self.setLayout(layout)
    
    '''
    Get all of the inputs that are used to create a new model.
    '''
    def getInputs(self, boxes, title):
        inputs = {}
        inputs['checkBoxes'] = boxes
        inputs['title'] = title
        return inputs
    
    '''
    Get all the check boxed buttons variable names and weather they have been clicked.
    @return: Dictionary mapping name of button variable to it's state.
    '''
    def getBoxes(self):
        # get all attributes from the class.
        classAttributes = dir(self)
        buttonVars = []
        for attr in classAttributes:
            # use only the button variables.
            if attr.startswith('cb'):
                btn = getattr(self, attr)
                buttonVars.append((attr, btn))
        return buttonVars 
                
    '''
    Sends the searched schema and table to the controller.
    The controller then Create a new Table model and sends it to the Table view.
    @param schema: Schema to look up in db.
    @param table: Table to look up in db. 
    @return: text from the two line edit slots. 
    @QtCore.pyqtSlot(): Send signals to other classes.
    '''
    def on_button_clicked(self):
        inputs = self.getInputs(self.getBoxes(), self.leTitle.text())
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


                    
                
                
                
            
            