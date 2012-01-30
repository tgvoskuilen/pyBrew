
from fermData  import Fermentable
from hopData   import Hop
from yeastData import Yeast
from quantity  import Quantity
from styleData import Style
from otherData import Other

import os
import csv
from datetime import date

from pyBrew.pyBrewMethods import GetFloat
from pyBrew.range import Range

###############################################################################
class Project(object):
    """
    Contains the essential and calculated data for each project
    """
    #----------------------------------------------------------------------
    def __init__(self, name='New Project'):
        #Core project data
        self.name = name
        self.brewDate = date.today().strftime("%m/%d/%Y")
        self.batchSize = 0.
        self.daysInPrimary = 0
        self.daysInSecondary = 0
        self.boilSize = 0.
        self.boilTime = 0
        self.tankLoss = 0.
        self.actualOG = 0.
        self.actualColor = 0
        self.actualFG = 0.
        self.otherIngredients = []        
        self.notes = ''
        self.fermentables = []
        self.hops = []
        self.yeast = Yeast() #TODO: make this a list?

        #Saved project display settings        
        self.hopFormulaName = 'Tinseth'
        self.style = Style()

        #Calculated project data
        self.calcOG = 1.
        self.totalColor = 0
        self.calcSRM = 0
        self.boilOG = 1.
        self.totalIBU = 0
        self.BUGU = 0.
        self.actualAtten = 0.
        self.actualABW = 0.
        self.actualABV = 0.
        self.actualCal = 0.
        self.calcAtten = Range((0.,0.))
        self.calcFG  = Range((0.,0.))
        self.calcABW = Range((0.,0.))
        self.calcABV = Range((0.,0.))
        self.calcCal = Range((0.,0.))

        
    #--------------------------------------------------------------------------
    def Export(self, filename=None):
        if filename is None:
                filename = os.getcwd() + '/' + self.name
                
        projFile = csv.writer(open(filename, 'w'))

        projFile.writerow(['Project Name', self.name])
        projFile.writerow(['Brew Date', self.brewDate])
        projFile.writerow(['Days in Primary', str(self.daysInPrimary)])
        projFile.writerow(['Days in Secondary', str(self.daysInSecondary)])
        projFile.writerow(['Batch Size (gallons)', str(self.batchSize)])
        projFile.writerow(['Boil Size (gallons)', str(self.boilSize)])
        projFile.writerow(['Boil Time (min)', str(self.boilTime)])
        projFile.writerow(['Tank Loss (gallons)', str(self.tankLoss)])
        projFile.writerow(['Actual OG', str(self.actualOG)])
        projFile.writerow(['Actual Color', str(self.actualColor)])
        projFile.writerow(['Actual FG', str(self.actualFG)])
        
        projFile.writerow(['Fermentables', str(len(self.fermentables))])
        for ferm in self.fermentables:
            projFile.writerow([ferm.name,
                               str(ferm.amount.Value()),
                               ferm.amount.Unit()])
            
        projFile.writerow(['Hops', str(len(self.hops))])
        for hop in self.hops:
            projFile.writerow([hop.name,
                               str(hop.amount.Value()),
                               hop.amount.Unit(),
                               str(hop.boiltime),
                               str(hop.aau),
                               hop.form])
        
        projFile.writerow(['Yeast', '1'])
        projFile.writerow([self.yeast.name])
        
        projFile.writerow(['Other Ingredients',
                           str(len(self.otherIngredients))])
        for other in self.otherIngredients:
            projFile.writerow([other.name,
                               str(other.amount.Value()), 
                               other.amount.Unit()])
            
        projFile.writerow(['Notes', self.notes])
                
    #----------------------------------------------------------------------            
    def Import(self, filename):
        try:
            projFile = csv.reader(open(filename, 'r'))
            fileData = []
            for row in projFile:
                fileData.append(row)
            
            #Extract data to project
            self.name = fileData[0][1]
            self.brewDate = fileData[1][1]
            self.daysInPrimary = GetFloat(fileData[2][1])
            self.daysInSecondary = GetFloat(fileData[3][1])
            self.batchSize = GetFloat(fileData[4][1])
            self.boilSize = GetFloat(fileData[5][1])
            self.boilTime = GetFloat(fileData[6][1])
            self.tankLoss = GetFloat(fileData[7][1])
            self.actualOG = GetFloat(fileData[8][1])
            self.actualColor = GetFloat(fileData[9][1])
            self.actualFG = GetFloat(fileData[10][1])

            fRow = 12
            nf = int(fileData[fRow-1][1])
            for f in range(fRow, fRow + nf):
                self.fermentables.append(Fermentable(fileData[f][0],
                                            Quantity(GetFloat(fileData[f][1]),
                                                     fileData[f][2])))
            
            hRow = fRow + nf + 1
            nh = int(fileData[hRow-1][1])
            for h in range(hRow, hRow + nh):
                self.hops.append(Hop(fileData[h][0],
                                     Quantity(GetFloat(fileData[h][1]),
                                              fileData[h][2]),
                                     GetFloat(fileData[h][3]),
                                     GetFloat(fileData[h][4]),
                                     fileData[h][5]))
            
            yRow = hRow + nh + 1
            ny = int(fileData[yRow-1][1])
            self.yeast = Yeast(fileData[yRow][0]) #Only support 1 yeast
            
            oRow = yRow + ny + 1
            no = int(fileData[oRow-1][1])
            for o in range(oRow, oRow + no):
                self.otherIngredients.append(Other(fileData[o][0],
                                            Quantity(GetFloat(fileData[o][1]),
                                            fileData[o][2])))
            
            nRow = oRow + no
            self.notes = fileData[nRow][1]

            return True
        except:
            return False
            
    
    
    #----------------------------------------------------------------------
    def CalcValues(self):
        """ Calculate parameters for the project based on core values """
        
        totalSize = self.batchSize + self.tankLoss
        self.calcOG = 1.
        self.totalColor = 0

        #Fermentation and Color
        for ferm in self.fermentables:
            self.calcOG += ferm.calcGravity(totalSize,self.batchSize)
            self.totalColor += ferm.calcColor(totalSize,self.batchSize)
            
        if self.batchSize == 0.:
            self.calcOG = 0.
            self.totalColor = 0
            
        self.calcSRM = round( 1.4922 * self.totalColor**0.6859 )
            
        for ferm in self.fermentables:
            ferm.calcPercent(self.calcOG)

        if self.boilSize != 0.:
            self.boilOG = round( (self.calcOG - 1.) * totalSize / 
                                  self.boilSize + 1., 3 )
        else:
            self.boilOG = self.calcOG

            
        #Hops/Bitterness
        self.totalIBU = 0
        for hop in self.hops:
            hop.calcUse(self.hopFormulaName, self.boilOG)
            self.totalIBU += hop.calcIBU(self.hopFormulaName, totalSize, 
                                         self.batchSize, self.calcOG)

        if self.calcOG > 1. and self.totalIBU > 0:
            self.BUGU = round(self.totalIBU / (1000. * (self.calcOG - 1.)), 2)
        else:
            self.BUGU = 0.

            
        #Yeast/Attenuation
        self.calcAtten = self.yeast.attenuation
        if self.yeast.name != '' and self.calcOG > 1.:
            self.calcFG  = (self.calcOG - 1.)*(1. - self.calcAtten/100.) + 1.
            self.calcABW = (76.08 * (self.calcOG - self.calcFG) /
                                 (1.775 - self.calcOG))
            self.calcABV = self.calcABW * self.calcFG / 0.794
            self.calcCal = self.calcCalories(self.calcABW, self.calcOG, 
                                             self.calcFG)
        else:
            self.calcFG  = Range((0.,0.))
            self.calcABW = Range((0.,0.))
            self.calcABV = Range((0.,0.))
            self.calcCal = Range((0.,0.))

        if self.actualOG > 1. and self.actualFG > 1.:
            self.actualAtten = round(100. * (1.- (self.actualFG - 1.) /
                                     (self.actualOG-1.)), 1)
            self.actualABW = round(76.08 * (self.actualOG - self.actualFG) /
                                   (1.775 - self.actualOG), 1)
            self.actualABV = round(self.actualABW * self.actualFG / 0.794, 1)
            self.actualCal = self.calcCalories(self.actualABW, self.actualOG,
                                               self.actualFG)
        else:
            self.actualAtten = 0.
            self.actualABW = 0.
            self.actualABV = 0.
            self.actualCal = 0.

    #----------------------------------------------------------------------
    def calcCalories(self, ABW, OG, FG): #TODO Move to methods
        """ Calculate the calories in a 16 oz serving """
        return (((6.9*ABW+4.*((0.1808*(668.72*OG-463.37-205.25*OG**2.) +
                     0.8192*(668.72*FG-463.37-205.25*FG**2.)) - 0.1)) *
                     FG * 3.55) * 16. / 12.)

    #----------------------------------------------------------------------
    def __eq__(self, other):
        """ Equality definition for a project """
        return (self.batchSize == other.batchSize and
                self.brewDate == other.brewDate and
                self.daysInPrimary == other.daysInPrimary and
                self.daysInSecondary == other.daysInSecondary and
                self.boilSize == other.boilSize and
                self.boilTime == other.boilTime and
                self.tankLoss == other.tankLoss and
                self.name == other.name and
                self.actualOG == other.actualOG and
                self.actualColor == other.actualColor and
                self.actualFG == other.actualFG and
                self.otherIngredients == other.otherIngredients and
                self.notes == other.notes and
                self.yeast == other.yeast and
                self.style == other.style and
                self.fermentables == other.fermentables and
                self.hops == other.hops)

    #----------------------------------------------------------------------
    def __ne__(self, other):
        """ Inequality definition for a project """
        return not self.__eq__(other)