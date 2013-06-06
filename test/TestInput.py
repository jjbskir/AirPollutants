import os
import sys

'''
Test to make sure input files were created to go into NONROAD program.
'''
class TestInput():
    
    '''
    Initialize.
    @param scenario: Name of a scenario that has been run.
    '''
    def __init__(self, _scenario):
        self.scenario = _scenario
        self.path = 'C:/Nonroad/%s/' % (_scenario)
        # directories to search through. Where input files are stored.
        self.dirs = ['ALLOCATE', 'POP', 'OPT']
        # dictionary to store data. Data that gets compared with others.
        self.dataDict = {}
        self.createTest()
    
    '''
    Create the dataDict to be tested with another TestInput scenario.
    @return: dataDict containing all of the info on the file structure.
    '''
    def createTest(self):
        for d in self.dirs:
            self.walk(self.path + d)
              
    '''
    Goes through the entire directory and records the file
    directories and file names.
    @param path: Path of directory to start looking through. 
    '''
    def walk(self, path):
        for root, dirs, files in os.walk(path):
            # clean up files and directories so that they do not contain the scenario title
            cleanedFiles = []
            for f in files:
                f = f.replace(self.scenario, '')
                cleanedFiles.append(f)    
            root = root.replace('C:/Nonroad/' + self.scenario, '')
            self.dataDict[root] = cleanedFiles   

    '''
    Compare two scenarios together
    '''
    def compare(self, _otherScenario):
        try:
            if self.dataDict == _otherScenario.dataDict:
                print 'Same Inputs'
            else:
                print 'Different Inputs'
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise   