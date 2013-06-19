from PyQt4 import QtGui

'''
Used for validating user inputs.
'''
class Validation:
    
    # string containing the error.
    errors = []
    
    '''
    Called when ever a error is made. Adds the error message to a list.
    @param msg: Error message.
    @return: False, indicating a error occured.  
    '''
    def error(self, msg):
        self.errors.append(msg)
        return False
    
    '''
    Used to get the errors from validation.
    When it is called it destroys the old errors and returns them.
    @return: list of errors.
    '''
    def getErrors(self):
        oldErrors = self.errors
        self.errors = []
        return oldErrors
    
    '''
    Validate title.
    @param title: Title to validate. Must be less then or equal to 8 characters.
    @return: True if no errors, false if title is greater then 8 characters, 
    first character is not a letter, or the title has spaces.
    '''
    def title(self, title):
        alphabetL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        alphabetU = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        if not title:
            self.error('Must enter a run title.')
        elif len(title) > 8:
            self.error('Title must be less than 9 characters.')
        elif title[0] not in alphabetL and title[0] not in alphabetU:
            self.error('Title`s first character must be letter.')
        elif ' ' in title:
            self.error('Title cannot contain spaces.')
        else:
            return True
    
    '''
    Validate run codes. Make sure they selecetd a feed stock and harvest activity.
    @param run_codes: run codes to validate.
    @return: True if more then 0 run codes, false if no run codes were submitted.  
    '''
    def runCodes(self, run_codes):
        if len(run_codes) > 0:
            return True
        else:
            return self.error('Must select a feed stock and activity.') 
        
        
        
                   