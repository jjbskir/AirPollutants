'''
Abstract test class for a outline to the others.
'''
class TestAbstract(object):
    
   
    '''
    @abstractmethod
    '''
    def __init__(self, _scenario):
        self.scenario = _scenario
        self.dataDict = {} 
    '''
    @abstractmethod
    '''
    def createTest(self):
        raise NotImplementedError
    
    '''
    @abstractmethod
    '''
    def compare(self, _otherScenario):
        raise NotImplementedError