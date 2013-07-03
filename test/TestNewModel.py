import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from view.NewModel import NewModel

'''
A class for testing creating a new model in the GUI.
'''
class TestNewModel(unittest.TestCase):

    '''Create the GUI'''
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.newModel = NewModel()
    
    '''
    Test the title line edit.
    '''
    def testTitle(self):
        self.newModel.leTitle.setText('title')
        self.assertEqual(self.newModel.leTitle.text(), 'title')
        self.newModel.leTitle.setText('reallyLongWord')
        self.assertEqual(self.newModel.leTitle.text(), 'reallyLongWord')
    
    '''
    Test ability to check check boxes.
    '''
    def testCheckBox(self):
        checkBoxes = self.newModel.getBoxes()
        for box in checkBoxes:
            var = box[1]
            self.assertEqual(var.checkState(), 0)
            var.setCheckState(2)
            self.assertEqual(var.checkState(), 2)
    
    '''
    test allocate() Used to show that allocation is being made from
    corn grain to ws and cs non-harvest.
        def allocate(self):
        try: 
            csAllocation = str(1.0 - float(self.leAllocCG.text()))
            self.leAllocCS.setText(csAllocation)
        except: 
            pass
    '''
    def testAllocate(self):
        # initially the cs le should be blank.
        self.assertEqual(self.newModel.leAllocCS.text(), '')
        # enter a number into the cg le.
        self.newModel.leAllocCG.setText('.25')
        self.newModel.allocate()
        # cs should be 1 - .25 = .75
        self.assertEqual(self.newModel.leAllocCS.text(), '0.75')
        # enter a input that makes no sense.
        self.newModel.leAllocCG.setText('a')
        self.newModel.allocate()
        # cs output should remain the same as before.
        self.assertEqual(self.newModel.leAllocCS.text(), '0.75')
        # enter a negative #.
        self.newModel.leAllocCG.setText('-.25')
        self.newModel.allocate()
        # 1.25 = 1 - (-.25). This is a error that will be caught in Validate.Validate()
        self.assertEqual(self.newModel.leAllocCS.text(), '1.25')
    
    '''
    Test getInputs, which is the data sent to the Controller.
        inputs['checkBoxes'] = boxes
        inputs['title'] = title
        inputs['fertilizers'] = fertilizers
        inputs['operations'] = operations
        inputs['alloc'] = alloc
    '''
    def testGetInputs(self):  
        m = self.newModel
        cbs = m.getBoxes()
        ferts = m.getFerts()
        
        # nothing has been entered or changed yet.
        inputs = m.getInputs(m.getBoxes(), m.leTitle.text(), m.getFerts(), m.operations, m.leAllocCG.text())           
        self.assertEqual(inputs.keys(), ['operations', 'alloc', 'checkBoxes', 'fertilizers', 'title'])
        self.assertEqual(inputs['title'], '')
        self.assertEqual(inputs['fertilizers'], ferts)
        for fert in inputs['fertilizers'].values():
            for f in fert: self.assertEqual(f[1].text(), '')
        self.assertEqual(inputs['checkBoxes'], cbs)
        for cb in inputs['checkBoxes']:
            self.assertEqual(cb[1].checkState(), 0)
        self.assertEqual(inputs['operations'], {'CG': [],
                                                'CS': [],
                                                'SG': [],
                                                'WS': []})
        self.assertEqual(inputs['alloc'], '')
           
        # check all of the cb and add a title. Shill change those 2 inputs. This is the generic entry.   
        m.leTitle.setText('reallyLongWord')
        m.selectAll.setCheckState(2)
        m.showAll(m.selectAll)
        inputs = m.getInputs(m.getBoxes(), m.leTitle.text(), m.getFerts(), m.operations, m.leAllocCG.text())           
        self.assertEqual(inputs['title'], 'reallyLongWord')
        self.assertEqual(inputs['fertilizers'], ferts)
        for fert in inputs['fertilizers'].values():
            for f in fert: self.assertEqual(f[1].text(), '')
        self.assertEqual(inputs['checkBoxes'], cbs)
        for cb in inputs['checkBoxes']:
            self.assertEqual(cb[1].checkState(), 2)
        self.assertEqual(inputs['operations'], {'CG': ['F', 'H', 'N', 'P', 'T'],
                                                'CS': ['F', 'H', 'N', 'T'],
                                                'SG': ['F', 'H', 'N', 'P', 'T'],
                                                'WS': ['F', 'H', 'N', 'T']})
        self.assertEqual(inputs['alloc'], '')
        
        # unselect the check boxes. Should remove them and the operations.
        m.selectAll.setCheckState(0)
        m.showAll(m.selectAll)
        inputs = m.getInputs(m.getBoxes(), m.leTitle.text(), m.getFerts(), m.operations, m.leAllocCG.text())           
        self.assertEqual(inputs['title'], 'reallyLongWord')
        self.assertEqual(inputs['fertilizers'], ferts)
        for fert in inputs['fertilizers'].values():
            for f in fert: self.assertEqual(f[1].text(), '')
        self.assertEqual(inputs['checkBoxes'], cbs)
        for cb in inputs['checkBoxes']:
            self.assertEqual(cb[1].checkState(), 0)
        self.assertEqual(inputs['operations'], {'CG': [],
                                                'CS': [],
                                                'SG': [],
                                                'WS': []})
  
    '''
    Test the get attrbiute fucntion. Give it a few random inputs and see what it produces.
    @attention: Can make this more comprehensive later.
    '''
    def testGetAttributes(self):
        m = self.newModel
        self.assertEqual(m.getAllAtributes('leTitle')[0][1], m.leTitle)
        self.assertEqual(m.getAllAtributes('leF_sg_an')[0][1], m.leF_sg_an)
        self.assertEqual(m.getAllAtributes('leF_cg_aa')[0][1], m.leF_cg_aa)
        self.assertEqual(m.getAllAtributes('leF_ws_ur')[0][1], m.leF_ws_ur)
        self.assertEqual(len(m.getAllAtributes('lblF_sg')), 5)

    '''
    test getFerts() Make sure it contains the correct feed stocks. and 
    has 5 input fertilizers.
    '''
    def testGetFerts(self):
        feedstock = ['CG', 'CS', 'WS', 'SG']
        fertsDist = self.newModel.getFerts()
        self.assertEqual(len(fertsDist), 4)
        for feed, fert in fertsDist.items():
            self.assertEqual(feed in feedstock, True)
    
    '''
    Test closing all of the fertlizer line edits and labels.
    '''
    def testCloseAllFerts(self):
        # start up. All ferts line edits and labels should be closed.
        feeds = ['cg', 'sg', 'ws', 'cs']
        for feed in feeds:
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), False)
            lbl = self.newModel.getAllAtributes('lblF_' + feed)
            self.assertEqual(lbl[0][1].isHidden(), False)
        self.newModel.closeAllFerts()
        for feed in feeds:
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), True)
            lbl = self.newModel.getAllAtributes('lblF_' + feed)
            self.assertEqual(lbl[0][1].isHidden(), True)
    
    '''
    Test showFertDist(). for the 4 feed stocks that use fertilizers.
    Needs both the feed stock cb and the fert cb to be clicked to show.
    So 4 possibilities. 
    '''
    def testShowFerts(self):
        feeds = ['cg', 'sg', 'ws', 'cs'] 
        for feed in feeds:
            # ShowFertDist called. Line edits should be closed b/c no check boxes are clicked yet.
            self.newModel.showFertDist(feed, self.newModel.cbSGF, self.newModel.cbSG)
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), True)
            lbls = self.newModel.getAllAtributes('lblF_' + feed)
            for l in lbls:
                self.assertEqual(l[1].isHidden(), True)
            
            # check both boxes to show ferts.
            self.newModel.cbSG.setCheckState(2)
            self.newModel.cbSGF.setCheckState(2)
            self.newModel.showFertDist(feed, self.newModel.cbSGF, self.newModel.cbSG)
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), False)
            lbls = self.newModel.getAllAtributes('lblF_' + feed)
            for l in lbls:
                self.assertEqual(l[1].isHidden(), False)
            
            # unclick the 2 cb to close the ferts.
            self.newModel.cbSG.setCheckState(0)
            self.newModel.cbSGF.setCheckState(0)
            self.newModel.showFertDist(feed, self.newModel.cbSGF, self.newModel.cbSG)
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), True)
            lbls = self.newModel.getAllAtributes('lblF_' + feed)
            for l in lbls:
                self.assertEqual(l[1].isHidden(), True)
            
            # check the cb fert, but don't check the feed cb. Closes the fert le.
            self.newModel.cbSG.setCheckState(0)
            self.newModel.cbSGF.setCheckState(2)
            self.newModel.showFertDist(feed, self.newModel.cbSGF, self.newModel.cbSG)
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), True)
            lbls = self.newModel.getAllAtributes('lblF_' + feed)
            for l in lbls:
                self.assertEqual(l[1].isHidden(), True)
            
            # don't check the fert cb, but click the feed cb. Closes th fert le.
            self.newModel.cbSG.setCheckState(2)
            self.newModel.cbSGF.setCheckState(0)
            self.newModel.showFertDist(feed, self.newModel.cbSGF, self.newModel.cbSG)
            ferts = self.newModel.getAllAtributes('leF_' + feed)
            for fert in ferts:
                self.assertEqual(fert[1].isHidden(), True)
            lbls = self.newModel.getAllAtributes('lblF_' + feed)
            for l in lbls:
                self.assertEqual(l[1].isHidden(), True)

    '''
    Test showAll(). The method should open or close all of the checkboxes.
    '''
    def testShowAll(self):
        checkBoxes = self.newModel.getBoxes()
        # should start off with everything open. This will close them all.
        self.newModel.selectAll.setCheckState(0)
        self.newModel.showAll(self.newModel.selectAll)
        for box in checkBoxes:
            # operation cb that are closed.
            if len(box[0]) > 4:
                self.assertEqual(box[1].isHidden(), True)
            # feed stock cb. Always shown.
            else:
                self.assertEqual(box[1].isHidden(), False)
                
        # open all of the checkboxes.
        self.newModel.selectAll.setCheckState(2)
        self.newModel.showAll(self.newModel.selectAll)
        for box in checkBoxes:
            # operation cb that are open.
            if len(box[0]) > 4:
                self.assertEqual(box[1].isHidden(), False)
            # feed stock cb. Always shown.
            else:
                self.assertEqual(box[1].isHidden(), False)

    '''
    Test showMore(). Runs through all of the checkboxes and decides which
    ones should be shown or closed.
    '''
    def testShowMore(self):
        feeds = ['cg', 'sg', 'ws', 'cs'] 
        checkBoxes = self.newModel.getBoxes()
        # should initially start with all of them closed, besides the feed stock cb.
        self.newModel.showMore()
        for box in checkBoxes:
            # operation cb that are closed.
            if len(box[0]) > 5:
                self.assertEqual(box[1].isHidden(), True)
            # operation cb that are closed.
            elif len(box[0]) == 5:
                self.assertEqual(box[1].isHidden(), True)
            # feed stock cb. Always shown.
            else:
                self.assertEqual(box[1].isHidden(), False)
        
        # check all of the feed stock cb. The upper operation cb should be shown.
        [getattr(self.newModel, 'cb'+feed.upper()).setCheckState(2) for feed in feeds]
        self.newModel.showMore()
        for box in checkBoxes:
            # operation cb that are closed.
            if len(box[0]) > 5:
                self.assertEqual(box[1].isHidden(), True)
            # operation cb that are open.
            elif len(box[0]) == 5:
                self.assertEqual(box[1].isHidden(), False)
            # feed stock cb. Always shown.
            else:
                self.assertEqual(box[1].isHidden(), False)
                
        # check all of the operation cb. Everything should be shown.
        [box[1].setCheckState(2) for box in checkBoxes if len(box[0]) == 5]
        self.newModel.showMore()
        for box in checkBoxes:
            # operation cb that are open.
            if len(box[0]) > 5:
                self.assertEqual(box[1].isHidden(), False)
            # operation cb that are open.
            elif len(box[0]) == 5:
                self.assertEqual(box[1].isHidden(), False)
            # feed stock cb. Always shown.
            else:
                self.assertEqual(box[1].isHidden(), False)
            
        

if __name__ == "__main__":
    unittest.main()

















