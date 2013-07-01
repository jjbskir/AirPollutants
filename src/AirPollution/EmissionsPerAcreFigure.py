from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *
import matplotlib.pyplot as plt
from scipy.stats import scoreatpercentile

"""
@comments: much of this plotting utility was taken from the following URL:
http://matplotlib.org/examples/pylab_examples/boxplot_demo2.html
"""

"""
Creates a graph for each air pollutant emmision. Calculates emissions per acre.
Saved as Figures/EmissionsPerAcre_'+pollutant+'.png
Each graph has the total amount of air pollutants for each feedstock.
X-axis: feedstock
Y-axis: pollutant emmisions per acre.
"""
class EmissionsPerAcreFigure():
    
    '''
    Create emmision graphs per a acre..
    @param db: Database.
    @param path: Directory path.
    '''
    def __init__(self, cont):
        self.path = cont.get('path')
        self.db = cont.get('db')
        self.documentFile = "EmissionsPerAcreFigure"
                    
    #define inputs/constants:  
        pollutantLabels = ['$NO_x$', '$NH_3$', '$CO$', '$SO_x$','$VOC$','$PM_{10}$','$PM_{2.5}$']
        
        feedstockList = ['Corn Grain','Switchgrass','Corn Stover','Wheat Straw']
        fList = ['CG','SG','CS','WS']
        pollutantList = ['NOx','NH3','CO','SOx','VOC','PM10','PM25']
        EtOHVals = [2.76, 89.6, 89.6, 89.6] #gallons per production (bu for CG, dry short ton for everything else)    
    
        queryTable = 'summedemissions'
    
        for pNum, pollutant in enumerate(pollutantList):
    #-----------------EXTRACT DATA FROM THE DATABASE-----------------    
            dataArray = self.__collectData__(queryTable, feedstockList, pollutant, EtOHVals)
    #-----------------PART 2, PLOT DATA----------------------------------
            #pretty plotting things
            fig = plt.figure(figsize=(8,6))
            canvas = FigureCanvas(fig)        
            self.ax1 = fig.add_subplot(111)
    #adjust this value to change the plot size
    #----------------------------------------------------------------
            plt.subplots_adjust(left=0.15, right=0.99, top=0.95, bottom=0.1)
    #---------------------------------------------------------------- 

    #-------create boxplot
            bp = plt.boxplot(dataArray, notch=0, sym='', vert=1, whis=1000)
                
            plt.setp(bp['boxes'], color='black')
            plt.setp(bp['whiskers'], color='black', linestyle='-')
            plt.yscale('log')
    
            plotTitle=pollutantLabels[pNum]
            axisTitle = '%s emissions  (g/acre)' % (pollutantLabels[pNum])
            
            self.__setAxis__(plotTitle, axisTitle, dataArray, fList)    
    #plot 95% intervals 
            perc95 = self.__plotInterval__(dataArray)
    
            fig.savefig(self.path + 'Figures/EmissionsPerAcre_'+pollutant+'.png', format = 'png')
    
            print pollutant
                
            
    
    def __collectData__(self, queryTable, feedstockList, pollutant, EtOHVals):
        data = []
        for fNum, feedstock in enumerate(feedstockList):
            '''
            emmissions per acre = (pollutant lbs) / (total acres)
            emmissions = pollutant / harv_ac
            SELECT (%s) / (harv_ac) FROM %s.%s WHERE harv_ac > 0.0 AND feedstock ilike '%s';
            % (pollutant,  self.db.schema, queryTable, feedstock)
            '''
            query = """
                    SELECT (%s) / (harv_ac) FROM %s.%s WHERE harv_ac > 0.0 AND feedstock ilike '%s';
                    """  % (pollutant, self.db.schema, queryTable, feedstock)
            emmisions = self.db.output(query, self.db.schema)
            data.append(emmisions)
             
        return data
    
    
    
    def __plotInterval__(self, dataArray):
    
        numFeed = 4
        numArray = array([x for x in range(numFeed)]) + 1 #index starts at 1, not zero
            
        #plot 95% interval
        perc95 = array([scoreatpercentile(dataArray[0],95), scoreatpercentile(dataArray[1],95),
                        scoreatpercentile(dataArray[2],95), scoreatpercentile(dataArray[3],95)])
                          
        #plot 5% interval
        perc5 = array([scoreatpercentile(dataArray[0],5), scoreatpercentile(dataArray[1],5),
                        scoreatpercentile(dataArray[2],5), scoreatpercentile(dataArray[3],5)])
                        
        plt.plot((numArray), perc95, '_', markersize=15, color='k')                 
        plt.plot((numArray), perc5, '_', markersize=15, color='k')
        
        
        
    """
    function to set axis titles and plot titles
    """
    def __setAxis__(self, plotTitle, axisTitle, dataArray, data_labels):
    # Add a horizontal grid to the plot
        self.ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                      alpha=0.7)
                      
        #determine limits of axis
        self.ax1.set_ylim(bottom=1e-07, top=1e-1)                  
        
        # Hide these grid behind plot objects
        self.ax1.set_axisbelow(True)
    
        self.ax1.set_ylabel(axisTitle, size=25, style='normal')    
        
    
        self.ax1.set_xticklabels(data_labels, size=25, style='normal')                         
    
