import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from src.Inputs import Inputs
from src.Validation import Validation
from view.NewModel import NewModel

'''
A class for testing creating inputs that go into the NONROAD and Air pollution model.
Data from the NewModel view is requested for in the Controller. Then the Controller gives 
this data to Input, which creates useful data for NONROAD and Air pollution model.
'''
class TestValidation(unittest.TestCase):

    '''Create the GUI'''
    def setUp(self):
        self.app = QApplication(sys.argv)
        
    '''
    Create Inputs. Have the computer select inputs and fill in line edits.
    Then return the inputs to be sent to Inputs, which creates useful data for NONROAD.
    @return: Inputs object.
    '''
    def createNewInputs_returnInputs(self):
        # add title
        nm = NewModel()
        nm.leTitle.setText('title')
        # add allocation
        nm.leAllocCG.setText('.25')
        # check every check box.
        nm.selectAll.setCheckState(2)
        nm.showAll(nm.selectAll)
        # add fertilizer distributions.
        ferts = nm.getAllAtributes('leF_')
        [fert[1].setText('.2') for fert in ferts]
        # create inputs
        inputs = nm.getInputs(nm.getBoxes(), nm.leTitle.text(), nm.getFerts(), nm.operations, nm.leAllocCG.text())
        return Inputs(inputs)
        
    '''   
    Create Inputs. Without anything being selected. Return inputs that will not work for NONROAD.
    @return: Inputs object.
    '''
    def createNewInputs_empty_returnInputs(self):
        nm = NewModel()
        # create inputs
        inputs = nm.getInputs(nm.getBoxes(), nm.leTitle.text(), nm.getFerts(), nm.operations, nm.leAllocCG.text())
        return Inputs(inputs)
    
    '''
    Test error() - Adds a error message to a list and return false to signal a error has occured.
    '''
    def testError(self):
        v = Validation()
        self.assertEqual(v.error('message'), False)
        self.assertEqual(v.errors, ['message'])
        v.error('cool')
        self.assertEqual(v.errors, ['message', 'cool'])
    
    '''
    Test getErrors() - Get all of the old errors and return to the user. Then create a new list to store errors.
    '''
    def testGetErrors(self):
        v = Validation()
        v.errors = []
        v.error('msg')
        v.error('cool')
        self.assertEqual(v.getErrors(), ['msg', 'cool'])
        self.assertEqual(v.errors, [])
    
    '''
    Test title() - Make sure title has been iputed correctly.
    '''
    def testTitle(self):
        v = Validation()
        v.errors = []
        # give a good title.
        i = self.createNewInputs_returnInputs()
        self.assertEqual(v.title(i.title), True)
        # empty title.
        i = self.createNewInputs_empty_returnInputs()
        self.assertEqual(v.title(i.title), False)
        self.assertEqual(v.errors[0], 'Must enter a run title.')
        # title greater then 8 characters.
        self.assertEqual(v.title('longTitle'), False)
        self.assertEqual(v.errors[1], 'Title must be less than 9 characters.')
        # first letter is not a letter.
        self.assertEqual(v.title('1title'), False)
        self.assertEqual(v.errors[2], 'Title`s first character must be letter.')
        # empty space in title
        self.assertEqual(v.title('title h'), False)
        self.assertEqual(v.errors[3], 'Title cannot contain spaces.')
        
   
    '''
    Test runCodes() - Make sure run_codes have been made correctly. Need at least 1 run_code to run model.
    '''
    def testrunCodes(self):
        v = Validation()
        v.errors = []
        # Give good run codes.
        i = self.createNewInputs_returnInputs()
        self.assertEqual(v.runCodes(i.run_codes), True)
        # Don't give any run_codes. 
        i = self.createNewInputs_empty_returnInputs()
        self.assertEqual(v.runCodes(i.run_codes), False)
        self.assertEqual(v.errors[0], 'Must select a feed stock and activity.')
   
    '''
    Test fertDist() - Test the fert distributions sum to 1 and are all numbers.
    '''
    def testFertDist(self):
        v = Validation()
        v.errors = []
        # good fertilizer distribution with values that sum to 1.
        dist =  {'CG': ['.2', '.2', '.2', '.2', '.2'], 'CS': ['.2', '.2', '.2', '.2', '.2'],
                'WS': ['.2', '.2', '.2', '.2', '.2'], 'SG': ['0', '.2', '.3', '.3', '.2']}
        self.assertEqual(v.fertDist(dist), True)
        # good fertilizer distribution with None.
        dist = {'CG': None, 'CS': None,
                'WS': None, 'SG': None}
        self.assertEqual(v.fertDist(dist), True)
        # does not sum to 1.
        dist = {'CG': ['0.1', '.1', '0.1', '0.1', '0.1'], 'CS': None,
                'WS': None, 'SG': None}
        self.assertEqual(v.fertDist(dist), False)
        self.assertEqual(v.errors[0], 'Distribion must sum to 1.')
        # does not sum to 1.
        dist = {'CG': ['0.1', '.1', '0.1', '0.1', '0.1'], 'CS': None,
                'WS': None, 'SG': ['1.1', '5.1', '0.1', '0.1', '0.1']}
        self.assertEqual(v.fertDist(dist), False)
        self.assertEqual(v.errors[1], 'Distribion must sum to 1.')
        # did not enter a number.
        dist = {'CG': ['0.1', 'cow', '0.1', '0.1', '0.1'], 'CS': None,
                'WS': None, 'SG': ['1.1', 'hey', '0.1', '0.1', '0.1']}
        self.assertEqual(v.fertDist(dist), False)
        self.assertEqual(v.errors[2], 'Must enter a number for fertilizer distributions.')


    
    '''
    Test ferts() - Make sure fertilizers were entered. Debugging.
    '''
    def testFerts(self):
        v = Validation()
        v.errors = []
        # good inputs.
        ferts = {'CGF': True, 'CSF': True, 'SGF': True, 'WSF': True}
        self.assertEqual(v.ferts(ferts), True)
        ferts = {'CGF': False, 'CSF': False, 'SGF': False, 'WSF': False}
        self.assertEqual(v.ferts(ferts), True)
        # extra input that shouln't be there.
        ferts = {'CGF': False, 'CSF': False, 'SGF': False, 'WSF': False, 'COOL': False}
        self.assertEqual(v.ferts(ferts), False)
        self.assertEqual(v.errors[0], 'Fertilizer Error.')
   
    '''
    Test pest() - 
    '''
    def testPest(self):
        v = Validation()
        v.errors = []
        # good inputs.
        pests =  {'CGP': True, 'SGP': True}
        self.assertEqual(v.pest(pests), True)
        pests =  {'CGP': False, 'SGP': False}
        self.assertEqual(v.pest(pests), True)
        # extra input shouldn't be there.
        pests =  {'CGP': False, 'SGP': False, 'cool': False}
        self.assertEqual(v.pest(pests), False)
        self.assertEqual(v.errors[0], 'Pesticide Error.')
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
        