'''
Created on Jul 23, 2013

@author: lcauser
'''
import unittest
from development.IrrigationAcres import IrrigationAcres

class Test(unittest.TestCase):

    def setUp(self):
        self.ir = IrrigationAcres('sgNew')

    def tearDown(self):
        pass

    '''
    Test irrigation_acres() - 
    '''
    def testIrrigation_acres(self):
        data = self.ir.irrigation_acres()
        self.assertEqual(len(data), 5902)
        self.assertEqual(data[0][1], 1568.947725)
        
    '''
    Test irrigationFuelConsumption() - 
    '''
    def testIrrigationFuelConsumption(self): 
        data = self.ir.irrigationFuelConsumption()
        self.assertEqual(len(data), 5902)
        self.assertEqual(data[0][1], 3689.0608)
        
    '''
    Test irrigationAcresPerc() - 
    '''
    def testIrrigationAcresPerc(self):
        acreData = self.ir.irrigation_acres()
        percData = self.ir.percent_of_irrigation()
        irrigationData = self.ir.irrigationAcresPerc()
        self.assertEqual(len(irrigationData), len(acreData))
        self.assertEqual(irrigationData[0][1], percData[0][2] * acreData[1][1])
        self.assertEqual(irrigationData[1][1], percData[0][2] * acreData[2][1])
        self.assertEqual(irrigationData[2][1], percData[0][2] * acreData[4][1])

    '''
    Test fuelConsumptionPerAcre() - 
    '''
    def testFuelConsumptionPerAcre(self):
        acresData = self.ir.irrigationAcresPerc()
        fuelConsData = self.ir.irrigationFuelConsumption()
        fuelPerAcreData = self.ir.fuelConsumptionPerAcre()
        self.assertEqual(len(fuelPerAcreData), len(acresData))
        #self.assertEqual(fuelPerAcreData[0][1], fuelConsData[0][1] / acresData[1][1])


    
        

if __name__ == "__main__":
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    