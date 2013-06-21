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
    Test ability to distribute to fertilizers.
    '''   
    def testFertilizers(self):
        ferts = self.newModel.getFert()
        for fert in ferts:
            var = fert[1]
            self.assertEqual(var.text(), '')
            var.setText('.2')
            self.assertEqual(var.text(), '.2')
    
    '''
    Test the submit button.
    '''
    def testButton(self):
        self.assertEqual(self.newModel.btnCreate.isDefault(), False)
        self.newModel.btnCreate.setDefault(True)
        self.assertEqual(self.newModel.btnCreate.isDefault(), True)

    '''
    Test the get attrbiute fucntion.
    '''
    def testGetAttributes(self):
        self.assertEqual(self.newModel.getAllAtributes('leTitle')[0][1], self.newModel.leTitle)
    
    '''
    Test getInputs, which is the data sent to the Controller.
    '''
    def testGetInputs(self):        
        boxes = self.newModel.getBoxes()
        
        self.newModel.leTitle.setText('reallyLongWord')
        
        ferts = self.newModel.getFert()
        for fert in ferts:
            var = fert[1]
            self.assertEqual(var.text(), '')
            var.setText('.2')
            self.assertEqual(var.text(), '.2')
            
        inputs = self.newModel.getInputs(boxes, self.newModel.leTitle.text(), ferts)
        self.assertEqual(inputs.keys(), ['checkBoxes', 'fertilizers', 'title'])
        self.assertEqual(inputs['title'], 'reallyLongWord')
        self.assertEqual(inputs['fertilizers'][0], ('leFeaa', self.newModel.leFeaa))
        fertaa = inputs['fertilizers'][0][1]
        self.assertEqual(fertaa.text(), '.2')
        self.assertEqual(inputs['checkBoxes'][0], ('cbCG', self.newModel.cbCG))
        cbSG = inputs['checkBoxes'][0][1]
        self.assertEqual(cbSG.checkState(), 0)



if __name__ == "__main__":
    unittest.main()


















