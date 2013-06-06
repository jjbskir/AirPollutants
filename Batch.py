from subprocess import Popen

'''
Batches files for running.
Keeps track of the master batch file, which runs the smaller batch files
for each run code.
'''
class Batch:
    
    '''
    Initiate Batch class by recording batch paths and creating the Document.
    @param path: Path to scenario directory.
    @param modelRunTitle: Title of the scenario.
    '''
    def __init__(self, cont):
        # path to batch directory.
        self.path = cont.get('path') + 'OPT/'
        # path to batch to be used in a batch file.
        self.batchPath = self.path.replace('/', '\\') 
        # master path to the batch file that keeps track of all the run_code batch files.
        self.masterPath = self.path + cont.get('modelRunTitle') + '.bat'
        # create scenario level batch file. Needs the file directory to be created before creating.
        self.scenarioBatchFile = None
        # current batch file being made.
        self.batchFile = None
            
    '''
    Create Batch File for each run_code. 
    @param run_code: Name of new batch file.
    '''              
    def initialize(self, run_code):
        self.scenarioBatchFile.write('\n')
        self.batchFile = open(self.path + run_code + '.bat', 'w')
        self.batchFile.write("cd C:\\NonRoad\n")          

    '''
    Add states to the batch file.
    To run a batch file in DOS for this model, type:
    >NONROAD.exe C:\\NONROAD\\NewModel\\OPT\\<run_code>\\<option_file.opt>
    @param state: state the batch file is running.
    @param run_code: run code. 
    '''
    def append(self, state, run_code):
        lines = "NONROAD.exe " + self.batchPath + run_code + '\\' + state + ".opt\n"
        self.batchFile.writelines(lines) 
    
    '''
    finish the batch file and add the finished batch file to the full 'Scenario' batch file.
    @param run_code: run code.  
    '''
    def finish(self, run_code):
        self.batchFile.close()        
        self.scenarioBatchFile.write("CALL " + "\"" + self.batchPath + run_code + '.bat\"\n')
    
    '''
    ****************************************
    **    Acess point to NONROAD model    **
    ****************************************
    Call master batch file.
    Runs NONROAD model through function.
    ''' 
    def run(self):
        p = Popen(self.masterPath)
        #wait for batch file to complete 
        p.wait()  
       
        
        
        