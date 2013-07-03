import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from src.Inputs import Inputs
from view.NewModel import NewModel
'''
A class for testing creating inputs that go into the NONROAD and Air pollution model.
Data from the NewModel view is requested for in the Controller. Then the Controller gives 
this data to Input, which creates useful data for NONROAD and Air pollution model.
'''
class TestInputs(unittest.TestCase):

    '''Create the GUI'''
    def setUp(self):
        self.app = QApplication(sys.argv)
    
    '''
    Create newModel GUI. Have the computer select inputs and fill in line edits.
    Then return the inputs to be sent to Inputs.
    @return: Inputs dictionary.
    '''
    def createNewModel_returnInputs(self):
        # add title
        nm = NewModel()
        nm.leTitle.setText('title')
        # add allocation
        nm.leAllocCG.setText('.25')
        # check every check box.
        nm.selectAll.setCheckState(2)
        nm.showAll(nm.selectAll)
        # create inputs
        inputs = nm.getInputs(nm.getBoxes(), nm.leTitle.text(), nm.getFerts(), nm.operations, nm.leAllocCG.text())
        return inputs
    
    '''   
    Create newModel GUI. Without anything being selected.
    @return: Inputs dictionary.
    '''
    def createNewModel_empty_returnInputs(self):
        nm = NewModel()
        # create inputs
        inputs = nm.getInputs(nm.getBoxes(), nm.leTitle.text(), nm.getFerts(), nm.operations, nm.leAllocCG.text())
        return inputs
        
    '''
    Test title variable. Make sure it gets created when the class is created.
    key == 'title'
    '''
    def testTitle(self):
        inputs = self.createNewModel_returnInputs()
        i = Inputs(inputs)
        self.assertEqual(i.title, 'title')
    
    '''
    Test createAllocation() - Allocates non-harvest emissions from corn grain to corn stover and wheat straw.
    key == 'alloc'
    alloc['CG'] = value
    '''
    def testCreateAllocation(self):
        # Inputs with values. CG is the value inputed.
        # CS and WE are 1-CG value.
        inputs = self.createNewModel_returnInputs()
        i = Inputs()
        alloc = i.createAllocation(inputs['alloc'])
        self.assertEqual(alloc['CG'], 0.25)
        self.assertEqual(alloc['CS'], 0.75)
        self.assertEqual(alloc['WS'], 0.75)
        
        # empty inputs. Should return the default values of allocating everything to cg.
        inputs = self.createNewModel_empty_returnInputs()
        i = Inputs()
        alloc = i.createAllocation(inputs['alloc'])
        self.assertEqual(alloc['CG'], 1)
        self.assertEqual(alloc['CS'], 0)
        self.assertEqual(alloc['WS'], 0)
    
    '''
    Test createRunCodes() - Creates run_codes, and which feedstocks should have fertilizer and pesticide 
    applided to them.
    key == 'checkBoxes'
    TODO: Create tests for private methods that are used in this method.
    '''
    def testCreateRunCodes(self):
        # Inputs with values. Should be all of the run_codes, b/c every box was selected.
        inputs = self.createNewModel_returnInputs()
        i = Inputs()
        run_codes, ferts, pestFeed = i.createRunCodes(inputs['checkBoxes'])
        allRunCodes = ['FR', 'CG_CH', 'CG_CN', 'CG_IC', 'CG_ID', 'CG_IG', 'CG_IL', 'CG_NH', 'CG_NN', 'CG_RH', 'CG_RN', 'CS_NT', 'CS_RT', 
                       'SG_H1', 'SG_H2', 'SG_H3', 'SG_H4', 'SG_H5', 'SG_H6', 'SG_H7', 'SG_H8', 'SG_H9', 'SG_H10', 
                       'SG_N1', 'SG_N2', 'SG_N3', 'SG_N4', 'SG_N5', 'SG_N6', 'SG_N7', 'SG_N8', 'SG_N9', 'SG_N10', 
                       'SG_T1', 'SG_T2', 'SG_T3', 'SG_T4', 'SG_T5', 'SG_T6', 'SG_T7', 'SG_T8', 'SG_T9', 'SG_T10', 
                       'WS_NT', 'WS_RT']
        self.assertEqual(run_codes, allRunCodes)
        self.assertEqual(ferts, {'CGF': True, 'CSF': True, 'SGF': True, 'WSF': True})
        self.assertEqual(pestFeed, {'CGP': True, 'SGP': True})
        
        # empty inputs. Should return an empty list, b/c no run_codes were selected.
        inputs = self.createNewModel_empty_returnInputs()
        i = Inputs()
        run_codes, ferts, pestFeed = i.createRunCodes(inputs['checkBoxes'])
        self.assertEqual(run_codes, [])
        self.assertEqual(ferts, {'CGF': False, 'CSF': False, 'SGF': False, 'WSF': False})
        self.assertEqual(pestFeed, {'CGP': False, 'SGP': False})
    
    '''
    Test createFertilizerDistribution() -
    key == 'fertilizers'
    '''
    def testCreateFertilizerDistribution(self):
        pass
    
    '''
    Test createOperations() - 
    key == 'operations'
    '''
    def testCreateOperations(self):
        pass
    
        
        
if __name__ == "__main__":
    TestInputs.main()