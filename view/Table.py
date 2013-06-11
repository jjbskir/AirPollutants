import sys
from PyQt4 import QtGui, QtCore

'''
Table view of the data.
'''
class Table(QtGui.QWidget):
    
    def __init__(self, data, headers, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        # create table model.               
        tableData = TableModel(data, headers, self)
        # create view out of the model
        view = QtGui.QTableView()
        view.setModel(tableData)
        # schema and table name on top of data table.
        schema = QtGui.QLabel('schema')
        self.leSchema = QtGui.QLineEdit()
        table = QtGui.QLabel('table')
        self.leTable = QtGui.QLineEdit()
        # layout of widget.
        layout = QtGui.QGridLayout()
        layout.addWidget(schema, 1, 0)
        layout.addWidget(self.leSchema, 1, 1)
        layout.addWidget(table, 2, 0)
        layout.addWidget(self.leTable, 2, 1)
        layout.addWidget(view, 4, 1)
        self.setLayout(layout)
         
        
"""
Model class that drives the population of tabular display
From abstract class QAbstractTableModel.
"""      
class TableModel(QtCore.QAbstractTableModel):

    '''
    Initate Table Model. Need to use abstract base class QAbstractTableModel.
    @param headers: Headers for each column.
    @param arrayData: An array of data to populate the table with.   
    @param parent: Send in parent to remove QTimer error. Useless otherwise.
    '''
    def __init__(self, data, headers, parent):
        super(TableModel, self).__init__(parent)
        self.headers = headers
        self.arrayData = data
 
    '''
    Add data to the table.
    @param newData: New data.
    '''
    def addData(self, newData):
        self.beginResetModel()
        self.arrayData.append(newData)
        self.endResetModel()
 
    '''
    @abstract: Parent QAbstractTableModel
    Counts the rows in the table.
    '''
    def rowCount(self, parent):
        return len(self.arrayData)
    
    '''
    @abstract: Parent QAbstractTableModel
    Counts the columns in the table
    '''
    def columnCount(self, parent):
        return len(self.arrayData[0])

    '''
    @abstract: Parent QAbstractTableModel
    Makes sure data in the table is ok.
    '''
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arrayData[index.row()][index.column()])

    '''
    @abstract: Parent QAbstractTableModel. Not nesceary for running.
    Used to populate the headers of the table.
    '''
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant() 
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant(int(section + 1))   
        
                
if __name__ == '__main__':
    arraydata = [['00','01','02'],
                ['10','11','12'],
                ['20','21','22']]
    headers = ['gas1', 'gas2', 'gas3']
    app = QtGui.QApplication(sys.argv)
    v = Table(arraydata, headers)
    sys.exit(app.exec_())
    
    
    
    
    
    
    
    
