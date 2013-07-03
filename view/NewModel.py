from PyQt4 import QtCore, QtGui
import itertools

'''
Widget for creating a new air pollution model.
'''
class NewModel(QtGui.QWidget):
    
    # container to emit signals to other classes.
    procDone = QtCore.pyqtSignal(dict)
    # operations.
    operations = {'CS': [], 'WS': [], 'CG': []}
    
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
        self.cbSG.stateChanged.connect(lambda: self.showFertDist('sg', self.cbSGF, self.cbSG))
        self.cbFR = QtGui.QCheckBox('Forest Residue', self)
        self.cbCS = QtGui.QCheckBox('Corn Stover', self)
        self.cbCS.clicked.connect(self.showMore)
        self.cbCS.stateChanged.connect(lambda: self.showFertDist('cs', self.cbCSF, self.cbCS))
        self.cbWS = QtGui.QCheckBox('Wheat Straw', self)
        self.cbWS.clicked.connect(self.showMore)
        self.cbWS.stateChanged.connect(lambda: self.showFertDist('ws', self.cbWSF, self.cbWS))
        self.cbCG = QtGui.QCheckBox('Corn Grain', self)
        self.cbCG.clicked.connect(self.showMore)
        self.cbCG.stateChanged.connect(lambda: self.showFertDist('cg', self.cbCGF, self.cbCG))
        self.selectAll = QtGui.QCheckBox('Check All', self)
        self.selectAll.clicked.connect(lambda: self.showAll(self.selectAll))
        # harvest methods.
        self.harvestMethods = QtGui.QLabel('Harvest Methods: ')
        
        '''
        # aa, an, as, ur, ns
        # labels. annhydrous_amonia, ammonium_nitrate, ammonium_sulfate, urea, nsol
        #self.lblFert1 = QtGui.QLabel('Fertilizer Distribution', self)
        #self.lblFert2 = QtGui.QLabel('Leave blank for default values.', self)
        self.fertaa = QtGui.QLabel('annhydrous_amonia', self)
        self.fertan = QtGui.QLabel('ammonium_nitrate', self)
        self.fertas = QtGui.QLabel('ammonium_sulfate', self)
        self.fertur = QtGui.QLabel('urea', self)
        self.fertns = QtGui.QLabel('nsol', self)
        '''
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
        self.rowCount += 2
        # add switch grass.
        self.addSG(layout)
        # add forest redidue.
        self.addFR(layout)
        # add corn stover.
        self.addCS(layout)
        # add wheat straw.
        self.addWS(layout)
        # add corn grain.
        self.addCG(layout)
        # non-harvest allocation.
        self.addNonHarvestAllocation(layout)
        # add submit button.
        self.addRow(layout, 'btnCreate')
        #layout.addWidget(self.btnCreate, 12, 1)
        # close all of the nested activity check boxes.
        self.showMore()
        self.setLayout(layout)
    
    '''
    Switch grass layout.
    '''
    def addSG(self, layout):
        # for switch grass and corn grain.
        self.cbSGH = QtGui.QCheckBox('Harvest', self)
        self.cbSGN = QtGui.QCheckBox('Non Harvest', self)
        self.cbSGT = QtGui.QCheckBox('Transportation', self)
        self.cbSGF = QtGui.QCheckBox('Fertilizer', self)
        self.cbSGF.stateChanged.connect(lambda: self.showFertDist('sg', self.cbSGF, self.cbSG))
        self.cbSGP = QtGui.QCheckBox('Pesticide', self)
        # switch grass fertilizers.
        self.lblF_sg = QtGui.QLabel('Switch Grass Fertilizer.', self)
        self.lblF_sg_an = QtGui.QLabel('ammonium_nitrate', self)
        self.lblF_sg_as = QtGui.QLabel('ammonium_sulfate', self)
        self.lblF_sg_ur = QtGui.QLabel('urea', self)
        self.lblF_sg_ns = QtGui.QLabel('nsol', self)
        self.leF_sg_an = QtGui.QLineEdit()
        self.leF_sg_as = QtGui.QLineEdit()
        self.leF_sg_ur = QtGui.QLineEdit()
        self.leF_sg_ns = QtGui.QLineEdit()
        # layout
        layout.addWidget(self.cbSG, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.cbSGH, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbSGN, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbSGT, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbSGF, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbSGP, self.rowCount, 1)
        self.rowCount += 1
        self.addRow(layout, 'lblF_sg_', False, 7, 1)
        layout.addWidget(self.lblF_sg, self.rowCount, 0)
        self.addRow(layout, 'leF_sg', False, 7, 1)
    
    '''
    Forest residue layout.
    '''
    def addFR(self, layout):
        layout.addWidget(self.cbFR, self.rowCount, 0)
        self.rowCount += 1
    
    '''
    Corn stover layout.
    '''
    def addCS(self, layout):
        # for corn stover.
        self.cbCSH = QtGui.QCheckBox('Harvest', self)
        self.cbCSH.clicked.connect(self.showMore)
        self.cbCSN = QtGui.QCheckBox('Non-Harvest', self)
        self.cbCSN.clicked.connect(self.showMore)
        self.cbCST = QtGui.QCheckBox('Transport', self)
        self.cbCSF = QtGui.QCheckBox('Fertilizer', self)
        self.cbCSF.stateChanged .connect(lambda: self.showFertDist('cs', self.cbCSF, self.cbCS))
        # harvest.
        self.cbCS_RT = QtGui.QCheckBox('Reduce Till', self)
        self.cbCS_NT = QtGui.QCheckBox('No Till', self)
        # irrigation.
        self.cbCS_ID = QtGui.QCheckBox('Diesel Irrigation', self)
        self.cbCS_IL = QtGui.QCheckBox('LPG Irrigation', self)
        self.cbCS_IC = QtGui.QCheckBox('CNG Irrigation', self)
        self.cbCS_IG = QtGui.QCheckBox('Gasoline Irrigation', self)
        # corn stover fertilizers.
        self.lblF_cs = QtGui.QLabel('Corn Stover Fertilizers.', self)
        self.lblF_cs_aa = QtGui.QLabel('annhydrous_amonia', self)
        self.lblF_cs_an = QtGui.QLabel('ammonium_nitrate', self)
        self.lblF_cs_as = QtGui.QLabel('ammonium_sulfate', self)
        self.lblF_cs_ur = QtGui.QLabel('urea', self)
        self.lblF_cs_ns = QtGui.QLabel('nsol', self)
        self.leF_cs_aa = QtGui.QLineEdit()
        self.leF_cs_an = QtGui.QLineEdit()
        self.leF_cs_as = QtGui.QLineEdit()
        self.leF_cs_ur = QtGui.QLineEdit()
        self.leF_cs_ns = QtGui.QLineEdit()
        # layout.
        layout.addWidget(self.cbCS, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.cbCSH, self.rowCount, 1)
        layout.addWidget(self.cbCS_RT, self.rowCount, 2)
        layout.addWidget(self.cbCS_NT, self.rowCount, 3)
        self.rowCount += 1
        layout.addWidget(self.cbCSN, self.rowCount, 1)
        layout.addWidget(self.cbCS_ID, self.rowCount, 2)
        layout.addWidget(self.cbCS_IL, self.rowCount, 3)
        layout.addWidget(self.cbCS_IC, self.rowCount, 4)
        layout.addWidget(self.cbCS_IG, self.rowCount, 5)
        self.rowCount += 1
        layout.addWidget(self.cbCST, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbCSF, self.rowCount, 1)
        self.rowCount += 1
        self.addRow(layout, 'lblF_cs_', False, 7, 1)
        layout.addWidget(self.lblF_cs, self.rowCount, 0)
        self.addRow(layout, 'leF_cs', False, 7, 1)
    
    '''
    Wheat straw layout.
    '''
    def addWS(self, layout):
        # for wheat straw.
        self.cbWSH = QtGui.QCheckBox('Harvest', self)
        self.cbWSH.clicked.connect(self.showMore)
        self.cbWSN = QtGui.QCheckBox('Non-Harvest', self)
        self.cbWSN.clicked.connect(self.showMore)
        self.cbWST = QtGui.QCheckBox('Transport', self)
        self.cbWSF = QtGui.QCheckBox('Fertilizer', self)
        self.cbWSF.stateChanged .connect(lambda: self.showFertDist('ws', self.cbWSF, self.cbWS))
        # harvest
        self.cbWS_RT = QtGui.QCheckBox('Reduce Till', self)
        self.cbWS_NT = QtGui.QCheckBox('No Till', self)
        # irrigation
        self.cbWS_ID = QtGui.QCheckBox('Diesel Irrigation', self)
        self.cbWS_IL = QtGui.QCheckBox('LPG Irrigation', self)
        self.cbWS_IC = QtGui.QCheckBox('CNG Irrigation', self)
        self.cbWS_IG = QtGui.QCheckBox('Gasoline Irrigation', self)
        # wheat straw fertilizers.
        self.lblF_ws = QtGui.QLabel('Wheat Straw Fertilizer.', self)
        self.lblF_ws_aa = QtGui.QLabel('annhydrous_amonia', self)
        self.lblF_ws_an = QtGui.QLabel('ammonium_nitrate', self)
        self.lblF_ws_as = QtGui.QLabel('ammonium_sulfate', self)
        self.lblF_ws_ur = QtGui.QLabel('urea', self)
        self.lblF_ws_ns = QtGui.QLabel('nsol', self)
        self.leF_ws_aa = QtGui.QLineEdit()
        self.leF_ws_an = QtGui.QLineEdit()
        self.leF_ws_as = QtGui.QLineEdit()
        self.leF_ws_ur = QtGui.QLineEdit()
        self.leF_ws_ns = QtGui.QLineEdit()
        # layout
        layout.addWidget(self.cbWS, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.cbWSH, self.rowCount, 1)
        layout.addWidget(self.cbWS_RT, self.rowCount, 2)
        layout.addWidget(self.cbWS_NT, self.rowCount, 3)
        self.rowCount += 1
        layout.addWidget(self.cbWSN, self.rowCount, 1)
        layout.addWidget(self.cbWS_ID, self.rowCount, 2)
        layout.addWidget(self.cbWS_IL, self.rowCount, 3)
        layout.addWidget(self.cbWS_IC, self.rowCount, 4)
        layout.addWidget(self.cbWS_IG, self.rowCount, 5)
        self.rowCount += 1
        layout.addWidget(self.cbWST, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbWSF, self.rowCount, 1)
        self.rowCount += 1
        self.addRow(layout, 'lblF_ws_', False, 7, 1)
        layout.addWidget(self.lblF_ws, self.rowCount, 0)
        self.addRow(layout, 'leF_ws', False, 7, 1)
    
    '''
    Corn grain layout.
    '''    
    def addCG(self, layout):
        # for corn grain. and Irrigation 
        self.cbCGH = QtGui.QCheckBox('Harvest', self)
        self.cbCGH.clicked.connect(self.showMore)
        self.cbCGN = QtGui.QCheckBox('Non-Harvest', self)
        self.cbCGN.clicked.connect(self.showMore)
        self.cbCGT = QtGui.QCheckBox('Transport', self)
        self.cbCGT.clicked.connect(self.showMore)
        self.cbCGF = QtGui.QCheckBox('Fertilizer', self)
        self.cbCGF.stateChanged .connect(lambda: self.showFertDist('cg', self.cbCGF, self.cbCG))
        self.cbCGP = QtGui.QCheckBox('Pesticide', self)
        # harvest.
        self.cbCG_CH = QtGui.QCheckBox('Conventional Till', self)
        self.cbCG_RH = QtGui.QCheckBox('Reduced Till', self)
        self.cbCG_NH = QtGui.QCheckBox('No Till', self)
        # non-harvest
        self.cbCG_CN = QtGui.QCheckBox('Conventional Till', self)
        self.cbCG_RN = QtGui.QCheckBox('Reduced Till', self)
        self.cbCG_NN = QtGui.QCheckBox('No Till', self)
        # irrigation
        self.cbCG_ID = QtGui.QCheckBox('Diesel Irrigation', self)
        self.cbCG_IL = QtGui.QCheckBox('LPG Irrigation', self)
        self.cbCG_IC = QtGui.QCheckBox('CNG Irrigation', self)
        self.cbCG_IG = QtGui.QCheckBox('Gasoline Irrigation', self)
        # corn grain fertilizer line edits.
        self.lblF_cg = QtGui.QLabel('Corn Grain Fertilizer.', self)
        self.lblF_cg_aa = QtGui.QLabel('annhydrous_amonia', self)
        self.lblF_cg_an = QtGui.QLabel('ammonium_nitrate', self)
        self.lblF_cg_as = QtGui.QLabel('ammonium_sulfate', self)
        self.lblF_cg_ur = QtGui.QLabel('urea', self)
        self.lblF_cg_ns = QtGui.QLabel('nsol', self)
        self.leF_cg_aa = QtGui.QLineEdit()
        self.leF_cg_an = QtGui.QLineEdit()
        self.leF_cg_as = QtGui.QLineEdit()
        self.leF_cg_ur = QtGui.QLineEdit()
        self.leF_cg_ns = QtGui.QLineEdit()
        # layout.
        layout.addWidget(self.cbCG, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.cbCGH, self.rowCount, 1)
        layout.addWidget(self.cbCG_CH, self.rowCount, 2)
        layout.addWidget(self.cbCG_RH, self.rowCount, 3)
        layout.addWidget(self.cbCG_NH, self.rowCount, 4)
        self.rowCount += 1
        layout.addWidget(self.cbCGN, self.rowCount, 1)
        layout.addWidget(self.cbCG_CN, self.rowCount, 2)
        layout.addWidget(self.cbCG_RN, self.rowCount, 3)
        layout.addWidget(self.cbCG_NN, self.rowCount, 4)
        self.rowCount += 1
        layout.addWidget(self.cbCG_ID, self.rowCount, 2)
        layout.addWidget(self.cbCG_IL, self.rowCount, 3)
        layout.addWidget(self.cbCG_IC, self.rowCount, 4)
        layout.addWidget(self.cbCG_IG, self.rowCount, 5)
        self.rowCount += 1
        layout.addWidget(self.cbCGT, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbCGF, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.cbCGP, self.rowCount, 1)
        self.rowCount += 1
        self.addRow(layout, 'lblF_cg_', False, 7, 1)
        layout.addWidget(self.lblF_cg, self.rowCount, 0)
        self.addRow(layout, 'leF_cg', False, 7, 1)
    
    '''
    def addFert(self, layout):
        # Fertilizer distribution.
        # line edits.

        # add to layout.
        layout.addWidget(self.lblFert1, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.lblFert2, self.rowCount, 0)
        self.rowCount += 1
        self.addRow(layout, 'fert', False, 7, 1)
    '''
    
    '''
    Add non-harvest allocation to layout.
    '''
    def addNonHarvestAllocation(self, layout):
        # labels. 
        self.lblAlloc1 = QtGui.QLabel('Allocate non-harvest emmisions from', self)
        self.lblAlloc2 = QtGui.QLabel('corn grain to corn stover and wheat straw.', self)
        self.lblAlloc3 = QtGui.QLabel('Enter a number from 0-1 representing the', self)
        self.lblAlloc4 = QtGui.QLabel('% of allocation to corn grain.', self)
        self.lblAlloc5 = QtGui.QLabel('Or leave blank for default values.', self)
        self.lblAlloc6 = QtGui.QLabel('Corn stover and', self)
        self.lblAlloc7 = QtGui.QLabel('wheat straw allocation', self)
        # line edits.
        self.leAllocCG = QtGui.QLineEdit()
        self.leAllocCG.textEdited.connect(self.allocate)
        self.leAllocCS = QtGui.QLineEdit()
        # add to layout.
        layout.addWidget(self.lblAlloc1, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.lblAlloc2, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.lblAlloc3, self.rowCount, 0)
        self.rowCount += 1
        layout.addWidget(self.lblAlloc4, self.rowCount, 0)
        layout.addWidget(self.lblAlloc6, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.lblAlloc5, self.rowCount, 0)
        layout.addWidget(self.lblAlloc7, self.rowCount, 1)
        self.rowCount += 1
        layout.addWidget(self.leAllocCG, self.rowCount, 0)
        layout.addWidget(self.leAllocCS, self.rowCount, 1)
        self.rowCount += 1

    '''
    Calculate the % of allocation going to ws and cs.
    @param leAllocCG: Corn grain allocation %.
    '''
    def allocate(self):
        try: 
            csAllocation = str(1.0 - float(self.leAllocCG.text()))
            self.leAllocCS.setText(csAllocation)
        except: 
            pass
        
    '''
    Add rows to the layout.
    @param layout: Layout to add widget to.
    @param attribute: Name of variable to look for.
    @param row: Used when a row was added without the help of addRow(). 
    Increases the row count to it's value. (int) 
    '''
    def addRow(self, layout, attribute, row=False, _colN=False, colStart=False):
        # change row count.
        if row:
            self.rowCount = row
        # change col count.
        if _colN: colN = _colN
        else: colN = 5
        if colStart: col = colStart
        else: col = 0
        widgets = self.getAllAtributes(attribute)
        # add all widgets with attribute to the row.
        for widget in widgets:
            if col == colN:
                col = 1
                self.rowCount += 1
            variable = widget[1]
            layout.addWidget(variable, self.rowCount, col)
            col += 1
        self.rowCount += 1
        
    '''
    Get all of the inputs that are used to create a new model.
    '''
    def getInputs(self, boxes, title, fertilizers, operations, alloc):
        inputs = {}
        inputs['checkBoxes'] = boxes
        inputs['title'] = title
        inputs['fertilizers'] = fertilizers
        inputs['operations'] = operations
        inputs['alloc'] = alloc
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
    Get fertilizer distributions from the four feedstocks.
    @return: dictionary of the different feedstocks and their fertilizer distribution. dict(string: set(string, QLineEdit))
    '''
    def getFerts(self):
        ferts = {}
        ferts['CG'] = self.getAllAtributes('leF_cg')
        ferts['CS'] = self.getAllAtributes('leF_cs')
        ferts['WS'] = self.getAllAtributes('leF_ws')
        ferts['SG'] = self.getAllAtributes('leF_sg') 
        return ferts        
              
    '''
    Sends the searched schema and table to the controller.
    The controller then Create a new Table model and sends it to the Table view.
    @param schema: Schema to look up in db.
    @param table: Table to look up in db. 
    @return: text from the two line edit slots. 
    @QtCore.pyqtSlot(): Send signals to other classes.
    '''
    def on_button_clicked(self):
        inputs = self.getInputs(self.getBoxes(), self.leTitle.text(), self.getFerts(), self.operations, self.leAllocCG.text())
        self.procDone.emit(inputs)
        
    '''
    Once a feed stock has been clicked, let the view see the activities for
    harvest that are associated with the feed stock.
    '''
    def showMore(self):
        checkBoxes = self.getBoxes()
        # list of operations to use. Don't actually use the SG in the model though. For constistency.
#        operation = {'CS': [None for i in range(0,6)], 'WS': [None for i in range(0,6)], 
#                     'CG': [None for i in range(0,6)], 'SG': [None for i in range(0,6)]}
        operation = {'CS': [], 'WS': [], 
                     'CG': [], 'SG': []}

        feedStock = 'Empty'
        #skip = ['FR', 'CS', 'WS', 'SG']
        skip = ['FR']
        btnState = 0
        # look at each check box alphebatically ordered. 
        for box in checkBoxes:
            name = box[0]
            var = box[1]
            # if the button is a feed stock then set states.
            if len(name) == 4:
                feedStock = name[-2:]
                if var.checkState() == 2: btnState = 2
                else: btnState = 0
            # if the button is for a operation.
            elif len(name) == 5 and feedStock in name:
                if btnState == 0: var.close()
                else: var.show()
                # add and remove to list if checked.
                operList = operation[feedStock]
                oper = name[-1]
                if var.checkState() == 2: 
                    if oper not in operList: operList.append(oper) 
                elif var.checkState() == 0:
                    if oper in operList: operList.remove(oper)
                                      
            # if the feed stock box is clicked, then go into this part.
            # relies on the fact that the list of checkBoxes is alphebetically ordered.
            # if the activity is clicked then show it. Else do not show the box.
            elif feedStock in name and len(name) > 5:
                # skip fr and sg b/c dont have different categories, or they are a part of the run_codes.
                if feedStock in skip:
                    if btnState == 0: var.close()
                    else: var.show()
                # check both it the feedstock and operation has been clicked. 
                else:
                    # save current operations for use in air model.
                    self.operations = operation
                    # show harvest buttons.
                    if 'H' in operation[feedStock] and btnState == 2 and (name[-1] == 'H' or name[-2:] == 'RT' or name[-2:] == 'NT'):
                        var.show()
                    # shor non-harvest buttons.
                    elif 'N' in operation[feedStock] and btnState == 2 and (name[-1] == 'N' or name[5] == 'I'):
                        var.show()
                    # or close buttons.
                    else: var.close()
    
    '''
    Show all of the check boxes and click them all.
    @param selectAll: selectALl check box. QCheckBox
    '''
    def showAll(self, selectAll):
        checkBoxes = self.getBoxes()
        showAll = selectAll.checkState()
        for box in checkBoxes:
            var = box[1]
            # if cb is checked, check all of the other cb's.
            if showAll == 2:
                var.setCheckState(2)
            # if the cb is not checked, un-check all of the other cb's.
            elif showAll == 0:
                var.setCheckState(0)
        # run to show or not show cb's correctly.
        self.showMore()
 
    '''
    Show fertilizer distribution. Shows or close line edits.
    @param feed: Feed stock. string
    @param cbFert: A fertilizer check box. When clicked, it sent a signal here and it's var here. QCheckBox. 
    @param cbFeed: Feedstock check box. QCheckBox 
    '''
    def showFertDist(self, feed, cbFert, cbFeed):
        # get fert line edits and labels.
        ferts = self.getAllAtributes('leF_' + feed)
        lbls = self.getAllAtributes('lblF_' + feed)
        # if either check box is not clicked, then close the ferts.
        if cbFeed.checkState() == 0 or cbFert.checkState() == 0:
            [l[1].close() for l in lbls]
            [f[1].close() for f in ferts]
        # if both check boxes are clicked, open the ferts.
        elif cbFeed.checkState() == 2 and cbFert.checkState() == 2:
            [l[1].show() for l in lbls]
            [f[1].show() for f in ferts]
    
    '''
    Close all of the fertilizers line edits and labels.
    '''
    def closeAllFerts(self):
        self.showFertDist('sg', self.cbSGF, self.cbSG)
        self.showFertDist('cs', self.cbCSF, self.cbCS)
        self.showFertDist('ws', self.cbWSF, self.cbWS)
        self.showFertDist('cg', self.cbCGF, self.cbCG)
        
            
            
                
                
                
            
            