import Container
import Batch
from model.Database import Database
import QueryRecorder as qr
from PyQt4 import QtCore

import Options as Opt
import Allocate as Alo
import Population as Pop
import UpdateDatabase
import FugitiveDust
import Chemical
import CombustionEmissions 
import Fertilizer
import SinglePassAllocation 
import NEIComparison
import EmissionsPerGalFigure
import RatioToNEIFigure
import ContributionFigure

'''
Drives program.
Global Variables: modelRunTitle, run_codes, path, db, qr.
All stored in a Container.
Temporary Global Variables: run_code, fips, state, episodeYear.
'''
class Driver:
    
    '''
    Save important variables for the running of the program.
    @param modelRunTitle: Scenario title.
    @param run_codes: Run codes to keep track of where you are in the program  
    '''
    def __init__(self, _modelRunTitle, run_codes, _db):
        # add run title.
        self.modelRunTitle = self._addTitle(_modelRunTitle)
        # add run codes.
        self.run_codes = run_codes
        # container to pass info around.
        self.cont = Container.Container()
        self.cont.set('modelRunTitle', self._addTitle(_modelRunTitle))
        self.cont.set('run_codes', run_codes)
        self.cont.set('path', 'C:/Nonroad/%s/' % (_modelRunTitle))
        self.cont.set('db', _db)
        self.cont.set('qr', qr.QueryRecorder(self.cont.get('path')))
        # create Batch runner.
        self.batch = Batch.Batch(self.cont)
    
    '''
    Make sure the program is less then 8 characters.
    Is not a run code.
    @param title: Title of the program.
    '''
    def _addTitle(self, title):
        assert len(title) <= 8
        return title
        
    '''
    Set up the NONROAD program by creating option, allocation, and population files.
    Also creates batch files to run.
    @attention: maybe should make episodeYear to be a global variable in this class instead of Options.
    '''    
    def setupNONROAD(self):
        #initialize objects
        scenario = Opt.ScenarioOptions(self.cont)
        alo = Alo.Allocate(self.cont)
        # create batch file.
        self.batch.getMaster('w')
                
        # go to each run code.
        for run_code in self.run_codes:
            
            print run_code
            #query database for appropriate production data based on run_code:
            # fips, state, productions 
            # @attention: should this return the data?
            scenario.getData(run_code)
               
            #initialize variables
            state = scenario.data[0][1]
            fips_prior = str(scenario.data[0][0])
            
            #New population object created for each run_code  
            # Pop is the abstract class and .<type> is the concrete class.  
            if run_code.startswith('CG_I'): pop = Pop.CornGrainIrrigationPop(self.cont, scenario.episodeYear, run_code)
            elif run_code.startswith('SG'): pop = Pop.SwitchgrassPop(self.cont, scenario.episodeYear, run_code)
            elif run_code.startswith('FR'): pop = Pop.ForestPop(self.cont, scenario.episodeYear, run_code)
            elif run_code.startswith('CS'): pop = Pop.ResiduePop(self.cont, scenario.episodeYear, run_code)
            elif run_code.startswith('WS'): pop = Pop.ResiduePop(self.cont, scenario.episodeYear, run_code)    
            elif run_code.startswith('CG'): pop = Pop.CornGrainPop(self.cont, scenario.episodeYear, run_code)
            
            # is it possible to instantiate new classes each time?
            alo.initializeAloFile(state, run_code, scenario.episodeYear)
            pop.initializePop(scenario.data[0])
            self.batch.initialize(run_code)
            
            # go through each row of the data table.
            for dat in scenario.data:
                fips = str(dat[0])
                '''
                The db table is ordered alphabetically.
                The search will look through a state. When the state changes in the table,
                then the loop will go to the else, closing the old files. and initializing new files.
                '''              
                if dat[1] == state:
                    indicator = dat[2]
                    alo.writeIndicator(fips, indicator)
                    pop.append_Pop(fips, dat)
                # last time through a state, will close different files, and start new ones.
                else:
                    #write *.opt file, close allocation file, close *.pop file            
                    Opt.NROptionFile(self.cont, state, fips_prior, run_code, scenario.episodeYear)
                    alo.writeSumAndClose(fips_prior)
                    self._popFinishHelper(pop, alo.inicatorTotal)
                    self.batch.append(state, run_code)
                            
                    fips_prior = fips
                    state = dat[1]   
        
                    #initialize new pop and allocation files.                      
                    alo.initializeAloFile(state, run_code, scenario.episodeYear)
                    pop.initializePop(dat)
                    indicator = dat[2]
                    alo.writeIndicator(fips, indicator)
                    pop.append_Pop(fips, dat)            
                 
            #close allocation files    
            Opt.NROptionFile(self.cont, state, fips_prior, run_code, scenario.episodeYear)        
            alo.writeSumAndClose(fips_prior)
            self._popFinishHelper(pop, alo.inicatorTotal)
            self.batch.append(state, run_code)
            self.batch.finish(run_code)
        
        #close scenariobatchfile
        self.batch.scenarioBatchFile.close()
        # save path for running batch files.
        # why is this here?
        self.path = scenario.path
    
    '''
    If the run code is CG_I, then another input parameter is needed
    to finishPop().
    '''
    def _popFinishHelper(self, pop, indicator):
        if not pop.run_code.startswith('CG_I'):
            pop.finishPop()
        else:
            pop.finishPop(indicator) 
     
    '''
    Run the NONROAD program by opening the batch files.
    @param qprocess: sub process controller from the Controller.
    Used to control the flow of the NONROAD program within the application.
    '''   
    def runNONROAD(self, qprocess):
        self.batch.run(qprocess) 
        
    '''
    Create and populate the schema with the emissions inventory.   
    '''
    def saveData(self, fertFeedStock, fertDist, pestFeed):
        print 'Saving results to database...'
        # initialize database objects
        Fert = Fertilizer.Fertilizer(self.cont, fertFeedStock, fertDist) 
        Chem = Chemical.Chemical(self.cont, pestFeed)
        Comb = CombustionEmissions.CombustionEmissions(self.cont)
        Update = UpdateDatabase.UpdateDatabase(self.cont)
        FugDust = FugitiveDust.FugitiveDust(self.cont)
        NEI = NEIComparison.NEIComparison(self.cont)
        
        # get feedstocks from the run_codes
        feedstockList = []
        for run_code in self.run_codes:
            if run_code[0:2] in feedstockList:
                pass
            else:
                feedstockList.append(run_code[0:2])
        
        
    #----------------------------------------------------------------
        #Create tables, Populate Fertilizer & Chemical tables.  
        for feedstock in feedstockList:
            Update.createTables(feedstock)
            Fert.setFertilizer(feedstock)
            Chem.setChemical(feedstock)
            print "Fertilizer and Chemical complete for " + feedstock
    #----------------------------------------------------------------
        
        
    #----------------------------------------------------------------    
        #Populate Combustion Emissions Tables
        print "Populating tables with combustion emissions..."
        Comb.populateTables(self.run_codes, self.modelRunTitle)
        print "...COMPLETED populating tables with combustion emissions."
    #----------------------------------------------------------------
        
        
    #----------------------------------------------------------------
        #Fugitive Dust Emissions
        modelSG = False
        for run_code in self.run_codes:
            if not run_code.startswith('SG'):
                FugDust.setEmissions(run_code) 
                print "Fugitive Dust Emissions complete for " + run_code  
            else: 
                modelSG = True
                
        if modelSG:
            #It makes more sense to create fugitive dust emissions using a separate method
            operations = ['Transport', 'Harvest', 'Non-Harvest']
            for operation in operations:
                sgFugDust = FugitiveDust.SG_FugitiveDust(self.cont, operation)
                sgFugDust.setEmissions()

    #only run the following if all feedstocks are being modeled.
        if len(feedstockList) == 5:
    #----------------------------------------------------------------
            #allocate emissions for single pass methodology - see constructor for ability to allocate CG emissions
            print "Allocate single pass emissions between corn stover and wheat straw."
            SinglePassAllocation.SinglePassAllocation(self.cont)
    #----------------------------------------------------------------
            
            
    #----------------------------------------------------------------
            #Create NEI comparison
            
            #create a single table that has all emissions in this inventory
            print 'populating Summed Dimmesnions table'
            for feedstock in feedstockList:
                NEI.createSummedEmissionsTable(feedstock)
                
            #create tables that contain a ratio to NEI
            for feedstock in feedstockList:
                NEI.createNEIComparison(feedstock)
    #----------------------------------------------------------------
    
    
    #----------------------------------------------------------------
            #create graphics and numerical summary 
            
            #Contribution Analysis
            ContributionFigure.ContributionAnalysis(self.cont)
            
            #Emissions Per Gallon
            EmissionsPerGalFigure.EmissionsPerGallon(self.cont)
            
            #Ratio to NEI
            ratioNEI = RatioToNEIFigure.RatioToNEIFig(self.cont)
            for feedstock in feedstockList:
                pass
            
            #create all feedstock and cellulosic NEI ratios
            if len(feedstock) == 5:
                pass
            
            ratioNEI.f.close()
    #----------------------------------------------------------------
                    
        print 'Successful completion of model run.'



if __name__ == "__main__":    
    
    # scenario title.
    title = 'folder'
    # run codes.
    run_codes = [
                     #'SG_H1','SG_H2','SG_H3','SG_H4','SG_H5','SG_H6','SG_H7','SG_H8','SG_H9','SG_H10',
                     #'SG_N1','SG_N2','SG_N3','SG_N4','SG_N5','SG_N6','SG_N7','SG_N8','SG_N9','SG_N10',
                     #'SG_T1','SG_T2','SG_T3','SG_T4','SG_T5','SG_T6','SG_T7','SG_T8','SG_T9','SG_T10',
                     #'FR',
                     'CS_RT','CS_NT',
                     #'WS_RT','WS_NT',
                     #'CG_CH','CG_CN',
                     #'CG_RH','CG_RN',
                     #'CG_NH','CG_NN',
                     #'CG_ID','CG_IL',
                     #'CG_IC','CG_IG'
                ] 
    # create databse.
    db = Database(title)
    qprocess = None
    # run program
    d = Driver(title, run_codes, db)
    d.setupNONROAD()
    d.runNONROAD(qprocess)
    #d.saveData()
    
        
        
        