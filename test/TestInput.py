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
        self.dirs = ['ALLOCATE', 'POP', 'OPT', 'OUT', 'QUERIES']
        # dictionary to store data. Data that gets compared with others.
        self.dataDict = {}
        self.createDict()
    
    '''
    Create the dataDict to be tested with another TestInput scenario.
    @return: dataDict containing all of the info on the file structure.
    '''
    def createDict(self):
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
    Multi directory search. Searches through all children directories
    and grabs content from files to compare with the file from other scenario.
    @param otherScenario: Other scenario to compare with.
    @param parentDirect: Parent directory to search through. 
    '''
    def multiDirectSearch(self, _otherScenario, paretnDirect):
        keys = self.dataDict.keys()
        same, different = 0, 0
        for direct in keys:
            if paretnDirect in direct:
                s, d = self.directorySearch(_otherScenario, direct)
                same += s
                different += d
        print 'Searched through directory %s with %s files and %s are different' % (paretnDirect, same, different)      
    
    '''
    Searches through every file in a directory for it's content
    and compares it to another scenarios file.
    @param otherScenario: Other scenario to comapre with.
    @param direct: Directory to search in.  
    '''
    def directorySearch(self, _otherScenario, _direct):
        # number of files that are different.
        different = 0
        direct = _direct
        path = self.path + direct + '/'
        pathOther = _otherScenario.path + direct + '/' 
        files = self.dataDict.get(direct)
        otherFiles = _otherScenario.dataDict.get(direct)
        if len(files) != len(otherFiles):
            print 'different number of files. %s vs %s' % (len(files), len(otherFiles))
        for i in range(len(files)):
            content = self._readLines(files[i], path, self.scenario)
            contentOther = self._readLines(otherFiles[i], pathOther, _otherScenario.scenario)
            if content != contentOther:
                different += 1
                print 'Different data in file: %s' % (files[i])
        print 'Searched through directory %s with %s files and %s are different' % (direct, i, different)
        return i, different
    
    '''
    Read the text from a file.
    @param fil: File's name to open and read.
    @param path: Path to open the file.   
    @return: The content in the file.
    '''
    def _readLines(self, fil, path, title):
        with open(path + fil) as f:
            content = f.readlines()
            cleanedContent = []
            for c in content:
                cleanedContent.append(c.replace(title, ''))
        return cleanedContent
    
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

if __name__ == "__main__":  
    ti1 = TestInput('AllFeed')
    ti2 = TestInput('fullRun')
    # inputs
    #ti1.directorySearch(ti2, '/ALLOCATE')
    #ti1.directorySearch(ti2, '/POP')
    ti1.multiDirectSearch(ti2, '/OPT\\')
    # outputs.
    #ti1.multiDirectSearch(ti2, '/OUT\\')
    #ti1.directorySearch(ti2, '/QUERIES')
    ti1.compare(ti2) 
    
    
    