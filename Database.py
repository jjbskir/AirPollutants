'''
Database.py - Database connection and querying.
@author: Jeremy Bohrer
@organization: NREL
@date: 6/2/2013
'''

import psycopg2 as db

class Database:
    
    '''
    Initialize the database and remember schemas.
    @param modelRunTitle: scenario title. Where emmision results are stored.
    '''
    def __init__(self, modelRunTitle):
        #credentials for connecting to the database -- superuser
        self.conn = self.connect()
        # schema name for production data
        self.productionSchema = 'BTS2dat_55'
        # schema name for stored constants (n application rates, n distribution, nei data, etc...)
        self.constantsSchema = 'constantvals'        
        # schema name for the scenario
        self.schema = modelRunTitle
        # schema for testing purposes.
        self.testSchema = None

    '''
    Connect to the database. Can either enter in credentials, or connect to predefined database.
    @param dbName: database name.
    @param user: user name.
    @param password: password.  
    '''
    def connect(self, _dbName=False, _user=False, _password=False):
        if _dbName != False and _user != False and _password !=False:
            dbName, user, password = _dbName, _user, _password
        else:
            dbName, user, password = 'biofuel', 'nfisher', 'nfisher'
        return db.connect("dbname=%s user=%s password=%s" % (dbName, user, password))

    '''
    used to execute a sql query that inserts data into the databse.
    @param query: sql insert query. 
    '''
    def input(self, query):   
        cur = self.conn.cursor()
        cur.execute("SET search_path to %s" % (self.schema))
        cur.execute(query)
        self.conn.commit()
        cur.close()

    '''
    Extract data from the database.
    @param query: sql extract query. 
    @return: rows extracted from database.
    '''
    def output(self, shema, query):
        cur = self.conn.cursor()
        cur.execute("SET search_path TO %s" % (shema))           
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows
    
    '''
    Close the database when done using.
    '''
    def close(self):
        self.conn.close()


if __name__ == "__main__":     
    db = Database('test')
    query = """select ca.fips, ca.st, dat.reducedtill_harv_ac, dat.reducedtill_prod, dat.reducedtill_yield
                from cs_data dat, """ + db.constantsSchema + """.county_attributes ca where dat.fips = ca.fips order by ca.fips asc"""
    data = db.output(db.productionSchema, query)
    db.close()
    print data
        
    
    
    
    
    
    
    