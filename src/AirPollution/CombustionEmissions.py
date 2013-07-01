import SaveDataHelper
import csv
import os

"""
Writes raw data for emmisions to a .csv file that can be opened with excel.
Then saves the data to the db with name <run_code>_raw.

Transform the data from the default Nonroad output to a useful format. 
Update database with emissions as well as copy emissions to static files
for quick debugging and error checking.  
Combustion emmisions associated with harvest and non-harvest methods that use non-road vehicles.
"""
class CombustionEmissions(SaveDataHelper.SaveDataHelper):
    
    '''
    @param operationDict: dictionary containing 3 feedstocks that have harvest, non-harvest, and transport.
    Each feedstock contains another dictionary of the harvest methods and weather to do the run with them.
    dict(dict(boolean))
    {'CS': {'H': True, 'N': True, 'T': True}, 
    'WS': {'H': True, 'N': True, 'T': True},
    'CG': {'H': True, 'N': True, 'T': True}}
    @param alloc: Amount of non harvest emmisions to allocate to cg, cs, and ws. dict(string: int)
    {'CG': .9, 'CS': .1, 'WS': .1}
    '''
    def __init__(self, cont, operationDict, alloc): 
        SaveDataHelper.SaveDataHelper.__init__(self, cont)
        self.documentFile = "CombustionEmissions"
        self.pmRatio = 0.20
        self.basePath = cont.get('path')
        # operations and feedstock dictionary.
        self.operationDict = operationDict
        self.alloc = alloc

    def populateTables(self, run_codes, modelRunTitle):
        
        #-------Inputs Begin
        # # 1 short ton (2000 lbs) = 0.90718474 tonne ( 1 Mg)
        convert_tonne = 0.9071847  # short ton / Metric ton
        
        # # DOE conversion from BTU/gal of diesel, LHV
        self.LHV = 128450.0 / 1e6  # mmBTU / gallon --> default for diesel fuel, changed for other fuel types
                
        # # RSF2 impact analysis NH3 emission factor
        self.NH3_EF = 0.68  # gNH3 / mmBTU --> default for diesel fuel, changed for other fuel types
        
        # # Convert THC to VOC
        self.vocConversion = 1.053  # --> default for diesel fuel
        
        # # Convert PM10 to PM2.5
        # not used at the moment...
        self.pm10toPM25 = 0.97  # --> default for diesel fuel
        #-------Inputs End
        
        for run_code in run_codes:
            
            print run_code
            # path to results
            path = self.basePath + 'OUT/%s/' % (run_code)
            listing = os.listdir(path)
        
            feedstock = run_code[0:2] 
            
            
            # write data to static files for debugging purposes
            f = open(self.basePath + 'OUT/' + run_code + '.csv', 'wb')
            writer = csv.writer(f)
            writer.writerow(('FIPS', 'SCC', 'HP', 'FuelCons_gal/yr', 'THC_exh', 'VOC_exh', 'CO_exh', 'NOx_exh',
                            'CO2_exh', 'SO2_exh', 'PM10_exh', 'PM25_exh', 'NH3_exh', 'Description'))
        
            queries = []
            for cur_file in listing:
                # use for debugging
                # print "Current file is: %s -- %s" % (run_code, cur_file)
                reader = csv.reader(open(path + cur_file))
         
                # account for headers in file, skip the first 10 lines.
                for i in range(10): reader.next()
                        
                for row in reader:
                    
                    if float(row[4]) > 0.0:    
                
                        # _getDescription updates the vocConversion, NH3_EF and LHV for each fuel type    
                        SCC = row[2]
                        HP = row[3]   
                        description, operation = self._getDescription(run_code, SCC, HP) 
                        # check if it is a feedstock and operation that should be recorded.
                        if feedstock == 'SG' or feedstock == 'FR' or self.operationDict[feedstock][operation[0]]:           
                        
                            THC = float(row[5]) * convert_tonne
                            CO = float(row[6]) * convert_tonne
                            NOx = float(row[7]) * convert_tonne
                            CO2 = float(row[8]) * convert_tonne
                            SO2 = float(row[9]) * convert_tonne
                            PM10 = float(row[10]) * convert_tonne
                            PM25 = float(row[10]) * 0.97 * convert_tonne
                            FuelCons = float(row[19])  # gal/year
                            
                            
                            VOC = THC * self.vocConversion * convert_tonne                    
                            NH3 = FuelCons * self.LHV * self.NH3_EF / (1e6)  # gal/year * mmBTU/gal * gNH3/mmBTU * Mg/g
                            
                            
                            # allocate non harvest emmisions from cg to cs and ws.
                            if operation and operation[0] == 'N' and feedstock == 'CG': 
                                # add to cs.
                                if self.operationDict['CS'][operation[0]]:
                                    self._record('CS', row[0], SCC, HP, FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3, description, run_code, writer, queries, self.alloc)
                                # add to ws. 
                                elif self.operationDict['WS'][operation[0]]:  
                                    self._record('WS', row[0], SCC, HP, FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3, description, run_code, writer, queries, self.alloc)
                                # add to corn grain.
                                self._record(feedstock, row[0], SCC, HP, FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3, description, run_code, writer, queries, self.alloc)
                            # don't change allocation.
                            else: 
                                self._record(feedstock, row[0], SCC, HP, FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3, description, run_code, writer, queries)
                            
                            # change constants back to normal, b/c they can be changes in _getDescription()
                            self.LHV = 128450.0 / 1e6  
                            self.NH3_EF = 0.68
                            self.vocConversion = 1.053
                            self.pm10toPM25 = 0.97
                        
            self.db.input(queries)
        
        print "Finished populating table for " + run_code            

    '''
    write data to static files and the database
    @param feed: Feed stock. string
    @param alloc: Allocation of non-harvest emmissions between cg, cs, and ws. dict(string: int)
    @param emmissions: Emmissions from various pollutants. int  
    '''
    def _record(self, feed, row, SCC, HP, FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3, description, run_code, writer, queries, alloc=None):
        # multiply the emmissions by allocation constant.
        if alloc:
            FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3 = FuelCons * alloc[feed], THC * alloc[feed], VOC * alloc[feed], CO * alloc[feed], NOx * alloc[feed], CO2 * alloc[feed], SO2 * alloc[feed], PM10 * alloc[feed], PM25 * alloc[feed], NH3 * alloc[feed]
        #writer.writerow((row, SCC, HP, FuelCons, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, NH3, run_code,))
                            
        q = """INSERT INTO %s.%s_raw (FIPS, SCC, HP, THC, VOC, CO, NOX, CO2, SOx, PM10, PM25, fuel_consumption, NH3, description, run_code) 
                                            VALUES ('%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', '%s')""" % (self.db.schema, feed, row, SCC, HP, THC, VOC, CO, NOx, CO2, SO2, PM10, PM25, FuelCons, NH3, description, run_code)
        queries.append(q)


    def _getDescription(self, run_code, SCC, HP):
        # cast HP as a number
        HP = int(HP)
        # in case operation does not get defined.
        operation = ''
        
# Switchgrass        
        if run_code.startswith('SG_H'):
            if len(run_code) == 4: 
                description = "Year %s - Harvest" % (run_code[4])  # year 1-9
            else:
                description = "Year %s - Harvest" % (run_code[4:6])  # year 10

        elif run_code.startswith('SG_N'):
            if len(run_code) == 4: 
                description = "Year %s - Non-Harvest" % (run_code[4])  # year 1-9
            else:
                description = "Year %s - Non-Harvest" % (run_code[4:6])  # year 10
                
        elif run_code.startswith('SG_T'):
            if len(run_code) == 4: 
                description = "Year %s - Transport" % (run_code[4])  # year 1-9
            else:
                description = "Year %s - Transport" % (run_code[4:6])  # year 10
                        
# Forest Residue            
        elif run_code.startswith('FR'):
            if HP == 600:
                description = "Loader Emissions"
            elif HP == 175:
                description = "Chipper Emissions"
        
# Corn Stover and Wheat Straw        
        elif run_code.startswith('CS') or run_code.startswith('WS'):
        
        # get tillage    
            if run_code.endswith('RT'):
                tillage = 'Reduced Till'
            elif run_code.endswith('NT'):
                tillage = 'No Till'    
            
            if SCC.endswith('5020'):
                operation = 'Harvest'
            elif SCC.endswith('5015'):
                operation = 'Transport'
            
            description = tillage + ' - ' + operation
            
        # Corn Grain
        elif run_code.startswith('CG'):
            
        # get tillage    
            if run_code.startswith('CG_R'): tillage = 'Reduced Till'
                
            elif run_code.startswith('CG_N'): tillage = 'No Till'    
                
            elif run_code.startswith('CG_C'): tillage = 'Conventional Till'
        
        # special case for irrigation    
            elif run_code.startswith('CG_I'):
        
                if run_code.endswith('D'):
                    tillage = 'Diesel Irrigation'
                    self.LHV = 128450.0 / 1e6  
                    self.NH3_EF = 0.68  
                    self.vocConversion = 1.053
                    self.pm10toPM25 = 0.97 
                                 
                elif run_code.endswith('L'):
                    tillage = 'LPG Irrigation'
                    self.LHV = 84950.0 / 1e6
                    self.NH3_EF = 0.0  # data not available
                    self.vocConversion = 0.995
                    self.pm10toPM25 = 1.0
                               
                elif run_code.endswith('C'):
                    tillage = 'CNG Irrigation'
                    self.LHV = 20268.0 / 1e6
                    self.NH3_EF = 0.0  # data not available
                    self.vocConversion = 0.004
                    self.pm10toPM25 = 1.0
                                        
                elif run_code.endswith('G'):
                    tillage = 'Gasoline Irrigation'
                    self.LHV = 116090.0 / 1e6
                    self.NH3_EF = 1.01        
                    self.vocConversion = 0.933         
                    self.pm10toPM25 = 0.92
            
            # get operation (harvest or non-harvest)                                                    
            if run_code.endswith('N') or run_code.startswith('CG_I'):
                operation = 'Non-Harvest'
                
            elif run_code.endswith('H'):
                # get operation (harvest or transport)
                if SCC.endswith('5020'):
                    operation = 'Harvest'
                elif SCC.endswith('5015'):
                    operation = 'Transport'
            
   
            description = tillage + ' - ' + operation    
         
        return description, operation 
    
    
    
