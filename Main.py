'''
Main source code. Where the program is run.
'''

from model.Database import Database
from model.Model import Model
from controller.Controller import Controller
import sys
from PyQt4 import QtGui, QtCore
from src.AirPollution.Driver import Driver
from development.SG_VOC import SG_VOC

if __name__ == "__main__": 
    
    '''
    # scenario title.
    title = 'sgNew'
    # run codes.
    run_codes = [
                     'SG_H1','SG_H2','SG_H3','SG_H4','SG_H5','SG_H6','SG_H7','SG_H8','SG_H9','SG_H10',
                     'SG_N1','SG_N2','SG_N3','SG_N4','SG_N5','SG_N6','SG_N7','SG_N8','SG_N9','SG_N10',
                     'SG_T1','SG_T2','SG_T3','SG_T4','SG_T5','SG_T6','SG_T7','SG_T8','SG_T9','SG_T10',
                     'FR',
                     'CS_RT', 'CS_NT',
                     'WS_RT', 'WS_NT',
                     'CG_CH', 'CG_CN',
                     'CG_RH', 'CG_RN',
                     'CG_NH', 'CG_NN',
                     'CG_ID', 'CG_IL',
                     'CG_IC', 'CG_IG'
                ] 
    
    # create databse.
    db = Database(title)
    qprocess = None
    # aa, an, as, ur, ns
    fertDist = {'CG': None, 'CS': None, 'WS': None, 'SG': None}
#    
#    fertDist = {'CG': ['.2', '.2', '.2', '.2', '.2'], 
#                'CS': ['.2', '.2', '.2', '.2', '.2'],
#                'WS': ['.2', '.2', '.2', '.2', '.2'],
#                'SG': ['0', '.4', '.2', '.2', '.2']}
    fertFeed = {'CSF': True, 'WSF': True, 'CGF': True, 'SGF': True}
    pestFeed = {'CGP': True, 'SGP': True}
    operationDict = {'CS': {'H': True, 'N': True, 'T': True}, 
                     'WS': {'H': True, 'N': True, 'T': True},
                     'CG': {'H': True, 'N': True, 'T': True},
                     'SG': {'H': True, 'N': True, 'T': True}}
    alloc = {'CG': 1, 'CS': 0, 'WS': 0}    
    
    # run program
    d = Driver(title, run_codes, db)
    #d.setupNONROAD()
    #d.runNONROAD(qprocess)
    d.saveData(fertFeed, fertDist, pestFeed, operationDict, alloc)
    
    '''
    db = Database(None)
    m = Model(db)
    
    app = QtGui.QApplication(sys.argv)
    myController = Controller(m)
    myController.show()
    sys.exit(app.exec_()) 
    
    

    
