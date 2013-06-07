import SaveDataHelper

'''
Used to update database to account for single pass machines when harvesting corn.
Before one pass was for the corn itself and the next pass was to pick up the leftovers on the ground.
In the future this may occur with one pass.
'''
class SinglePassAllocation(SaveDataHelper.SaveDataHelper):
    
    def __init__(self, cont):
        SaveDataHelper.SaveDataHelper.__init__(self, cont)
        self.documentFile = "SinglePassAllocation"
        # 540 is the total energy allocation for the single pass allocation
        # 380 of it goes to the residue harvesting and 160 of it goes toward the corn harvesting.
        self.residueAllocation = str(380.0 / 540.0)
        self.cornGrainAllocation = str(160.0 / 540.0)
        '''
        @attention: allocateCG never gets called...
        so the second query is never made either...
        '''
        # weather to do corn grain or residue.
        self.allocateCG = False
        
        residues = ['cs','ws']
        
        '''
        @attention: should be able to combine the queries into one query. 
        The second query might never be called...
        '''
        #define corn stover query - 380/540
        for r in residues: 
            query = """
                UPDATE """+r+"""_raw
                SET
                    fuel_consumption = fuel_consumption * """+self.residueAllocation+""",
                    thc = thc * """+self.residueAllocation+""",
                    voc = voc * """+self.residueAllocation+""",
                    co = co * """+self.residueAllocation+""",
                    nox = nox * """+self.residueAllocation+""",
                    co2 = co2 * """+self.residueAllocation+""",
                    sox = sox * """+self.residueAllocation+""",
                    pm10 = pm10 * """+self.residueAllocation+""",
                    pm25 = pm25 * """+self.residueAllocation+""",
                    nh3 = nh3 * """+self.residueAllocation+""",
                    fug_pm10 = fug_pm10 * """+self.residueAllocation+""",
                    fug_pm25 = fug_pm10 * """+self.residueAllocation+"""
                WHERE description ilike '%Harvest%';
            """             
            self._executeQuery(query)
            
        #define corn grain query - 160/540
        if self.allocateCG:
            query = """
                UPDATE """+r+"""_raw
                SET
                    fuel_consumption = fuel_consumption * """+self.cornGrainAllocation+""",
                    thc = thc * """+self.cornGrainAllocation+""",
                    voc = voc * """+self.cornGrainAllocation+""",
                    co = co * """+self.cornGrainAllocation+""",
                    nox = nox * """+self.cornGrainAllocation+""",
                    co2 = co2 * """+self.cornGrainAllocation+""",
                    sox = sox * """+self.cornGrainAllocation+""",
                    pm10 = pm10 * """+self.cornGrainAllocation+""",
                    pm25 = pm25 * """+self.cornGrainAllocation+""",
                    nh3 = nh3 * """+self.cornGrainAllocation+""",
                    fug_pm10 = fug_pm10 * """+self.cornGrainAllocation+""",
                    fug_pm25 = fug_pm10 * """+self.cornGrainAllocation+"""
                WHERE 
                    description NOT ilike '%Conventional%' AND
                    description ilike '% Harvest%';
            """            
            self._executeQuery(query)
        
        
        
        
        
    