from PyQt4 import QtCore, QtGui

'''
Widget for creating a new air pollution model.
'''
class NewModel(QtGui.QWidget):
    
    # container to emit signals to other classes.
    procDone = QtCore.pyqtSignal(tuple)
    
    '''
    Add input forms to page
    '''
    def __init__(self, parent=None):
        super(NewModel, self).__init__(parent)
        
        lblS = QtGui.QLabel('new model', self)
        
        # layout
        layout = QtGui.QGridLayout()
        layout.addWidget(lblS, 1, 0)
        self.setLayout(layout)