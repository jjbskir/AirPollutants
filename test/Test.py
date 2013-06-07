'''
Test.py - used to test weather a scenario was correct.
@author: Jeremy Bohrer
@organization: NREL
@date: 6/2/2013
'''

from TestInput import TestInput 
import TestDB 
      
if __name__ == "__main__":  
    
    # from run codes CS_RT','CS_NT'.
    # uses a test scenario in the db called 'test' that contains info from cs_nfert, cs_raw, and summedemissions.  
    t = TestDB.TestDB('woh', 'AllFeed')
    # create the test two classes.
    test = t.getScenario(t.testSchema)
    new = t.getScenario(t.schema)
    print "testing new scenario results... \n"
    # compare scenarios.
    t.compareScenarios(new, test)
    
    
    ti1 = TestInput('woh')
    ti2 = TestInput('AllFeed')
    print ti1.dataDict
    print ti2.dataDict
    ti1.compare(ti2)
    
    
    
    
    
    