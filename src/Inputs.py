'''
Creates run codes.
'''
class Inputs:
    
    def __init__(self, inputs):
        self.sortInputs(inputs)
        
    '''
    Go through a dictionary of values that map a category to input parameters 
    to the air model.
    @param inputs: Input parameters to model. 
    title => run title.
    checkBoxes => run codes.
    @return: run codes and title.
    '''
    def sortInputs(self, inputs):
        for key, value in inputs.items():
            if key == 'title':
                self.title = value
            elif key == 'checkBoxes':
                self.run_codes = self.createRunCodes(value)
    
    '''
    Create run codes from the check boxes in the NewModel view.
    @param checkBoxes: A list of checkboxes. Each element is a tuple
    containing the name of the variable, which is used to determine
    the feed stock and harvest activity; and the checkbox variable
    to check weather it was checked or not.
    @return: The run codes used in the air model. 
    '''           
    def createRunCodes(self, checkBoxes):
        run_codes = []
        feedStock = []
        # 
        for checkBox in checkBoxes:
            name, var = checkBox[0], checkBox[1]
            if len(name) == 4 and var.checkState() == 2:
                # get the last two letters of the string.
                name = name[-2:]
                if name == 'FR':
                    run_codes.append(name) 
                else:
                    feedStock.append(name)
                    checkBoxes.remove(checkBox)
        for checkBox in checkBoxes:
            name, var = checkBox[0], checkBox[1]
            run_code = [feed + name[-3:] for feed in feedStock if feed in name and var.checkState() == 2]
            if run_code:
                run_code = run_code[0]
                if 'SG' not in run_code:
                    run_codes.append(run_code)
                else:
                    [run_codes.append(run_code[0:4] + str(i)) for i in range(1, 11)]
        return run_codes

            
            