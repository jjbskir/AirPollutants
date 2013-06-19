import SaveDataHelper

'''
Used to populate the newly created schema that stores emmision info.
Inserts data into cg_chem for emmisions from chemicals.
Created from pesticides.
'''
class Chemical(SaveDataHelper.SaveDataHelper):
    
    '''
    @attention: Only need db parts from OptionsScenario.
    will need schema variabls.
    '''
    def __init__(self, cont):
        SaveDataHelper.SaveDataHelper.__init__(self, cont)
        self.documentFile = "Chemical"
         
    '''
    Find the feedstock and add emmissions if it is switch grass or corn grain.
    @param feed: Feed stock.
    '''
    def setChemical(self, feed):
        
        if feed == 'CG' or feed == 'SG': 
            if feed == 'CG':
                query = self.__cornGrain__()
                
            elif feed == 'SG':
                query = self.__switchgrass__()
                
            self._executeQuery(query)
            
        
        
    '''
    emmisions = harvested acres * lbs/acre * Evaporation rate * VOC content (lbs VOC / lb active ingridient) * lbs active / lb  VOC
    emmisions = total VOC emmisions (lbs VOC).
    total_harv_ac = total harvested acres. (acres)
    pest.EF = lbs VOC/acre.
    .9 =  evaporation rate. lbs pesticide/lbs VOC
    .835 = lbs VOC / lb active ingridient.
    .9070 = lbs active / lbs pesticide.
    (acres) * (lbs VOC/acre) * (lbs pesticide/lbs VOC)? * (lbs VOC/lbs active) * (lbs active/lbs pesticide) = lbs VOC
    '''
    def __cornGrain__(self):
        chemQuery = """
INSERT INTO cg_chem
    (

    SELECT cg.fips, (2461850051) AS "SCC", 

    ((cg.total_harv_ac * pest.EF * 0.9 * 0.835) * 0.907018474 / 2000.0) AS "VOC", 

    ('Pesticide Emissions') AS "Description"

    FROM """+self.db.productionSchema+""".cg_data cg, """ + self.db.constantsSchema + """.CG_pest_app_factor pest

    WHERE substr(fips, 1, 2) = pest.STFIPS
    )"""
        return chemQuery
    

    '''
    Recieves several different fertilizers: Quinclorac, Attrazine, 2 and 4-D-Amine
    Multiply by .1 b/c it is switch grass on a ten year cycle.
    emmisions = .1 * harvested acres * lbs/acre * Evaporation rate * VOC content (lbs VOC / lb active ingridient) * lbs active / lb  VOC
    emmisions (lbs VOC)
    '''                                     
    def __switchgrass__(self):
        
        chemQuery = """
INSERT INTO sg_chem 
    (
        SELECT sg.fips, (2461850099) AS "SCC",  
        (
            (
            sg.harv_ac * 0.1 * (0.5) + 
            sg.harv_ac * 0.1 * (1.0) + 
            sg.harv_ac * 0.1 * (1.0) + 
            sg.harv_ac * 0.1 * (1.5)
            ) * 0.9 * 0.835
        ) * 0.90718474 / 2000.0 AS "VOC", 
     
        ('Establishment Year: quinclorac + Atrazine + 2-4-D-Amine') AS "Description"

        FROM """+self.db.productionSchema+""".sg_data sg
    )"""
        return chemQuery
          
        