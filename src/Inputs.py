'''
Creates run codes.
'''
class Inputs:
    
    # variables that can be accesed.
    title, run_codes, ferts, pestFeed, fertDist = None, None, None, None, None
    
    def __init__(self, inputs):
        self.sortInputs(inputs)
        
    '''
    Go through a dictionary of values that map a category to input parameters 
    to the air model.
    @param inputs: Input parameters to model. 
    title => run title.
    checkBoxes => run codes, and fertilizers.
    fertilizers => fertilizers distribution.
    @return: run codes, title, fertilizers, fertilizer distribution.
    '''
    def sortInputs(self, inputs):
        for key, value in inputs.items():
            if key == 'title':
                self.title = value
            elif key == 'checkBoxes':
                self.run_codes, self.ferts, self.pestFeed = self.createRunCodes(value)
            elif key == 'fertilizers':
                self.fertDist = self.createFertilizerDistribution(value)
    
    '''
    Create run codes from the check boxes in the NewModel view.
    @param checkBoxes: A list of checkboxes. Each element is a tuple
    containing the name of the variable, which is used to determine
    the feed stock and harvest activity; and the checkbox variable
    to check weather it was checked or not.
    @return: The run codes used in the air model. list(string)
    @return: Dictinary of each fertilizer and weather it was checked. dict(boolean)
    '''           
    def createRunCodes(self, checkBoxes):
        run_codes = []
        ferts = {}
        pestFeed = {}
        feedStock = self._getCheckedFeed(checkBoxes, run_codes)
        # go through every check box.
        for checkBox in checkBoxes:
            name, var = checkBox[0], checkBox[1]  
            run_code = self._makeRunCode(name, var, feedStock)
            if run_code:
                # if it is a run_code.
                if run_code[2] == '_':
                    if 'SG' not in run_code:
                        run_codes.append(run_code)
                    else:
                        [run_codes.append(run_code[0:4] + str(i)) for i in range(1, 11)]
                # if it is a fertilizer.
                elif run_code[2] == 'f':
                    if var.checkState() == 2: ferts[run_code[-3:]] = True
                    else: ferts[run_code[-3:]] = False
                elif run_code[2] == 'p':
                    if var.checkState() == 2: pestFeed[run_code[-3:]] = True
                    else: pestFeed[run_code[-3:]] = False
        return run_codes, ferts, pestFeed
    
    '''
    Get all of the checked feed stocks.
    @param checkBoxes: Check boxes from the NewModel GUI.
    @param run_codes: List that contains all of the run_codes that have been checked.
    Needed to add FR to it.
    @return: A list of all the checked feedstocks. list(string)
    '''
    def _getCheckedFeed(self, checkBoxes, run_codes):
        feedStock = []
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
        return feedStock
    
    '''
    Make a run code.
    @param name: Name of the variable.
    @param var: Compute memory of the variable to use.
    @param feedStock: The feed stock.
    @return: run_code. string
    '''
    def _makeRunCode(self, name, var, feedStock):
        run_code = ''
        # check every check box to make sure that it's feed stock has been chosen.
        for feed in feedStock:
            # if the box has been check.
            if feed in name and var.checkState() == 2:
                run_code = feed + name[-3:]
                pass
            # if the box has not been checked, but it is a fertilizer.
            elif len(name) >= 5 and name[5] == 'f':
                run_code = feed + name[-3:]
                pass
            # if the box has not been checked, but is a pesticide.
            elif len(name) >= 5 and name[5] == 'p':
                run_code = feed + name[-3:]
                pass
        return run_code
    
    '''
    Create fertilizer distribution. Needs to be ordered exactly for later.
    aa, an, as, ur, ns
    @param fertilizers: Feritlizers name and variable from NewModel.
    @return: fertilizer distribution the user entered or False if they did not enter anything. list(string)
    '''
    def createFertilizerDistribution(self, fertilizers):
        fertDist = []
        for fert in fertilizers:
            name, var = fert[0], fert[1]
            if name == 'leFeaa' and var.text(): fertDist[0] = str(var.text())
            elif name == 'leFean' and var.text(): fertDist[1] = str(var.text())
            elif name == 'leFeas' and var.text(): fertDist[2] = str(var.text())
            elif name == 'leFeur' and var.text(): fertDist[3] = str(var.text())
            elif name == 'leFens' and var.text(): fertDist[4] = str(var.text())
        # check if nothing was entered.
        if all(v == None for v in fertDist):
            return None
        return fertDist
            

            
            