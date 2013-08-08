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
        # add fertilizer distributions.
        ferts = nm.getAllAtributes('leF_')
        [fert[1].setText('.2') for fert in ferts]
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
        
        inputs = self.createNewModel_empty_returnInputs()
        i = Inputs(inputs)
        self.assertEqual(i.title, '')
    
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
        # inputs with values. Should be all of the run_codes, b/c every box was selected.
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
    Test createFertilizerDistribution() - Creates the fertilizer distribution for each feedstock. 
    Allows unique numbers for 5 different fertilizer types. Except switch grass does not use anhydrate.
    key == 'fertilizers'
    '''
    def testCreateFertilizerDistribution(self):
        # inputs with values. Each feedstock and fertilizer should have a value, except aa for switch grass.
        inputs = self.createNewModel_returnInputs()
        i = Inputs() 
        fertDist = i.createFertilizerDistribution(inputs['fertilizers'])
        self.assertEqual(fertDist, {'CG': ['.2', '.2', '.2', '.2', '.2'], 'CS': ['.2', '.2', '.2', '.2', '.2'],
                                    'WS': ['.2', '.2', '.2', '.2', '.2'], 'SG': ['0', '.2', '.2', '.2', '.2']})
        
        
        # empty inputs. Should return None for each feedstock, b/c no fertilizers where entered.
        inputs = self.createNewModel_empty_returnInputs()
        i = Inputs()
        fertDist = i.createFertilizerDistribution(inputs['fertilizers'])
        self.assertEqual(fertDist, {'CG': None, 'CS': None,
                                    'WS': None, 'SG': None})
             
    '''
    Test createOperations() - For each feedstock determine which operations out of harvest, non-harvest, and transport
    are used in the model.
    key == 'operations'
    '''
    def testCreateOperations(self):
        # inputs with values. For each feedstock and operation should be True.
        inputs = self.createNewModel_returnInputs()
        i = Inputs() 
        operationDict = i.createOperations(inputs['operations'])
        self.assertEqual(operationDict, {'CS': {'H': True, 'N': True, 'T': True}, 
                         'WS': {'H': True, 'N': True, 'T': True},
                         'CG': {'H': True, 'N': True, 'T': True},
                         'SG': {'H': True, 'N': True, 'T': True}})
        
        # empty inputs. Should return False for each feedstock and operation.
        inputs = self.createNewModel_empty_returnInputs()
        i = Inputs()
        operationDict = i.createOperations(inputs['operations'])
        self.assertEqual(operationDict, {'CS': {'H': False, 'N': False, 'T': False}, 
                         'WS': {'H': False, 'N': False, 'T': False},
                         'CG': {'H': False, 'N': False, 'T': False},
                         'SG': {'H': False, 'N': False, 'T': False}})
    
    '''
    Test __init__(). An overall test to make sure all needed variables get created.
    '''
    def test__init__(self):
        # inputs with values. For each feedstock and operation should be True.
        inputs = self.createNewModel_returnInputs()
        i = Inputs(inputs)
        self.assertEqual(i.title, 'title')
        self.assertEqual(i.alloc['CG'], 0.25)
        self.assertEqual(i.alloc['CS'], 0.75)
        self.assertEqual(i.alloc['WS'], 0.75)
        allRunCodes = ['FR', 'CG_CH', 'CG_CN', 'CG_IC', 'CG_ID', 'CG_IG', 'CG_IL', 'CG_NH', 'CG_NN', 'CG_RH', 'CG_RN', 'CS_NT', 'CS_RT', 
                       'SG_H1', 'SG_H2', 'SG_H3', 'SG_H4', 'SG_H5', 'SG_H6', 'SG_H7', 'SG_H8', 'SG_H9', 'SG_H10', 
                       'SG_N1', 'SG_N2', 'SG_N3', 'SG_N4', 'SG_N5', 'SG_N6', 'SG_N7', 'SG_N8', 'SG_N9', 'SG_N10', 
                       'SG_T1', 'SG_T2', 'SG_T3', 'SG_T4', 'SG_T5', 'SG_T6', 'SG_T7', 'SG_T8', 'SG_T9', 'SG_T10', 
                       'WS_NT', 'WS_RT']
        self.assertEqual(i.run_codes, allRunCodes)
        self.assertEqual(i.ferts, {'CGF': True, 'CSF': True, 'SGF': True, 'WSF': True})
        self.assertEqual(i.pestFeed, {'CGP': True, 'SGP': True})
        self.assertEqual(i.fertDist, {'CG': ['.2', '.2', '.2', '.2', '.2'], 'CS': ['.2', '.2', '.2', '.2', '.2'],
                                    'WS': ['.2', '.2', '.2', '.2', '.2'], 'SG': ['0', '.2', '.2', '.2', '.2']})
        self.assertEqual(i.operations, {'CS': {'H': True, 'N': True, 'T': True}, 
                         'WS': {'H': True, 'N': True, 'T': True},
                         'CG': {'H': True, 'N': True, 'T': True},
                         'SG': {'H': True, 'N': True, 'T': True}})
        
        # empty inputs. Should return False for each feedstock and operation.
        inputs = self.createNewModel_empty_returnInputs()
        i = Inputs(inputs)
        self.assertEqual(i.title, '')
        self.assertEqual(i.alloc['CG'], 1)
        self.assertEqual(i.alloc['CS'], 0)
        self.assertEqual(i.alloc['WS'], 0)
        self.assertEqual(i.run_codes, [])
        self.assertEqual(i.ferts, {'CGF': False, 'CSF': False, 'SGF': False, 'WSF': False})
        self.assertEqual(i.pestFeed, {'CGP': False, 'SGP': False})
        self.assertEqual(i.fertDist, {'CG': None, 'CS': None,
                                    'WS': None, 'SG': None})
        self.assertEqual(i.operations, {'CS': {'H': False, 'N': False, 'T': False}, 
                         'WS': {'H': False, 'N': False, 'T': False},
                         'CG': {'H': False, 'N': False, 'T': False},
                         'SG': {'H': False, 'N': False, 'T': False}})
        

        
if __name__ == "__main__":
    TestInputs.main()
    
    
    
    
    
    
    