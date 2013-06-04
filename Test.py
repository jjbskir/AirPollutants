'''
Test.py - used to test weather a scenario was correct.
@author: Jeremy Bohrer
@organization: NREL
@date: 6/2/2013
'''

import Database

'''
Uses a test schema and a new scenario schema from the database
and tests to see if the data is the same. 
@inherits Database.Database: Inherits database class for querying data.
'''
class Test(Database.Database):
    
    '''
    Inherit from database to grab test data.
    @param newSchema: New scenario to test if correct.
    @param testSchema: Test schema that we know is allready correct.
    '''
    def __init__(self, _newSchema, _testSchema):
        Database.Database.__init__(self, _newSchema)
        self.testSchema = _testSchema

    '''
    Get a specific scenario. 
    @param shema: Where the data for the scenario is stored in the db.
    @return: A representation of the schema in a dictionary. 
    Contains a mapping of the schema's tables to it's data. 
    '''
    def getScenario(self, schema):
        tables = self.getTables(schema)
        dataMap = self.queryData(schema, tables)
        return dataMap

    '''
    Get all of the table names from a schema.
    @param schema: Schema to look for table names.
    @return: All of the table names from a schema.  
    '''
    def getTables(self, schema):
        tableNameId   = 2
        query = """select * from information_schema.tables 
                   where table_schema = '%s'""" % (schema)
        data = self.output(self.testSchema, query)
        tables = [ row[tableNameId] for row in data]
        return tables

    '''
    Query all of the data from a schema.
    @param schema: Schema, to know where to grab data from.
    @param tables: Tables to find data in.  
    @return: Dictionary of tables names to their data.
    '''
    def queryData(self, schema, tables):
        # map of each data table to its data.
        dataMap = {}
        for table in tables:
            query = 'SELECT * FROM ' + table
            data = self.output(schema, query)
            dataMap[table] = data
        return dataMap
    
    '''
    Compares two scenarios and checks if they are the same or not.
    @param scenarioNew: New scenario.
    @param scenarioTest: Test scenario.
    @return: True if they have the same results, False otherwise. 
    '''
    def compareScenarios(self, scenarioNew, scenarioTest):
        if scenarioNew != scenarioTest:
            print "scenarios are not the same :("
            return False
        else:
            print "scenarios are the same!"
            return True
                
if __name__ == "__main__":  
    # uses a test scenario in the db called 'test' that contains info from cs_nfert, cs_raw, and summedemissions.  
    t = Test('new', 'test')
    # create the test two classes.
    test = t.getScenario(t.testSchema)
    new = t.getScenario(t.schema)
    print "testing new scenario results... \n"
    # compare scenarios.
    t.compareScenarios(new, test)
    
    
    
    
    