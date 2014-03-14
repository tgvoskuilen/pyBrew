"""
Copyright (c) 2012, Tyler Voskuilen
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from fermentable  import Fermentable
from hop   import Hop
from yeast import Yeast
from quantity  import Quantity
from style import Style
from other import Other
from brewfile import BrewFile

import os
import re
from datetime import date

from pyBrew.pyBrewMethods import GetFloat
from pyBrew.pyBrewMethods import NumString
from pyBrew.pyBrewMethods import ReadLine
from pyBrew.range import Range

###############################################################################
class Project(BrewFile):
    """
    Contains the essential and calculated data for each project
    
    'path' input here can be either full path to file, or just file name
    """
    #----------------------------------------------------------------------
    def __init__(self, path):
        BrewFile.__init__(self, path, 'proj')

        self.otherIngredients = []        
        self.fermentables = []
        self.hops = []
        self.style = Style()
        self.batchSize = 0.
        self.daysInPrimary = 0
        self.daysInSecondary = 0
        self.boilSize = 0.
        self.boilTime = 0
        self.tankLoss = 0.
        self.actualOG = 0.
        self.actualColor = 0
        self.actualFG = 0.      
        self.notes = ''
        self.yeast = Yeast() #TODO: make this a list?
        self.hopFormulaName = 'Rager'
        
        
        if not self.name:
            # Read project from existing file
            self.ReadFile()
            
        else:
            # Make new project
            self.brewDate = date.today().strftime("%b %d, %Y")
            self.WriteFile()

        #Calculated project data (not saved, calculated on load)
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
        
   
    
    #----------------------------------------------------------------------            
    def ReadFile(self):
        """
        Reads project file
        """
        
        try:
            lines = self.GetLines()
            self.name = self.GetTitle(lines)

            self.CheckName()
            
            sections = self.GetSections(lines)

            #Load section by section
            if "Project Summary" in sections:
                for line in sections['Project Summary']:

                    if 'Brew Date' in line:
                        spl = line.strip().split(' ')
                        date = ' '.join(spl[2:]).strip()
                        self.brewDate = date
                        
                    if 'days in primary' in line.lower():
                        days = ReadLine(line.lower(), "days in primary")
                        self.daysInPrimary = int(GetFloat(days[0]))
                        
                    if 'days in secondary' in line.lower():
                        days = ReadLine(line.lower(), "days in secondary")
                        self.daysInSecondary = int(GetFloat(days[0]))
            
                    if 'batch size' in line.lower():
                        amt, unit = ReadLine(line.lower(), "batch size")
                        self.batchSize = GetFloat(amt) #TODO Use Quantity()
            
                    if 'boil size' in line.lower():
                        amt, unit = ReadLine(line.lower(), "boil size")
                        self.boilSize = GetFloat(amt) #TODO Use Quantity()
                        
                    if 'tank loss' in line.lower():
                        amt, unit = ReadLine(line.lower(), "tank loss")
                        self.tankLoss = GetFloat(amt) #TODO Use Quantity()
                        
                    if 'boil time' in line.lower():
                        amt, unit = ReadLine(line.lower(), "boil time")
                        self.boilTime = int(GetFloat(amt)) #TODO Use Quantity()
                        
                    if 'project style' in line.lower():
                        spl = line.strip().split(' ')
                        stylename = ' '.join(spl[2:]).strip()
                        self.style = Style(stylename)
                        
                        
                        
            if "Fermentation Summary" in sections:
                reading_ferm_list = False
                for line in sections['Fermentation Summary']:
                    
                    if reading_ferm_list and not line.strip():
                        reading_ferm_list = False
                    
                    if reading_ferm_list:
                        self.fermentables.append( self.ReadFermentable(line) )

                    else:
                        if 'Actual OG' in line:
                            amt, unit = ReadLine(line, "Actual OG")
                            self.actualOG = GetFloat(amt)
                            
                        if 'Actual FG' in line:
                            amt, unit = ReadLine(line, "Actual FG")
                            self.actualFG = GetFloat(amt)
                            
                        if 'Actual Color' in line:
                            amt, unit = ReadLine(line, "Actual Color")
                            self.actualColor = int(GetFloat(amt))
                            
                        if 'Yeast' in line:
                            spl = line.split()
                            name = ' '.join(spl[1:])
                            self.yeast = Yeast(name.strip())
                               
                    if 'Fermentables List' in line:
                        reading_ferm_list = True
                        
            if "Hops Summary" in sections:
                reading_hop_list = False
                for line in sections['Hops Summary']:
                    
                    if reading_hop_list and not line.strip():
                        reading_hop_list = False
                    
                    if reading_hop_list:
                        self.hops.append( self.ReadHop(line) )                        
                        
                    else:
                        if 'Hop Formula' in line:
                            spl = line.strip().split(' ')
                            formula = ' '.join(spl[2:]).strip()
                            self.hopFormulaName = formula
                               
                    if 'Hops List' in line:
                        reading_hop_list = True     
                        
                        
            if "Other Ingredients" in sections:
                for line in sections["Other Ingredients"]:
                    self.otherIngredients.append( self.ReadOther(line) )
                
                
            if "Notes" in sections:
                self.notes = ''.join(sections['Notes'])
                
                
            return True
            
        except IOError:
            return False
            
    #--------------------------------------------------------------------------
    def WriteFile(self):
 
        f = open(self.path, 'w')
        self.WriteHeader(f)
        
        self.WriteSection(f, 'Project Summary')

        self.WriteArg(f, 'Brew Date', self.brewDate)
        self.WriteArg(f, 'Days in Primary', NumString(self.daysInPrimary,'Int'))
        self.WriteArg(f, 'Days in Secondary', NumString(self.daysInSecondary,'Int'),'\n')
        
        if self.style.name:
            self.WriteArg(f, 'Project style', self.style.name, '\n')
        
        self.WriteArg(f, 'Batch size', str(self.batchSize), 'gallons')
        self.WriteArg(f, 'Boil size', str(self.boilSize), 'gallons')
        self.WriteArg(f, 'Boil time', str(self.boilTime), 'min')
        self.WriteArg(f, 'Tank loss', str(self.tankLoss), 'gallons')
        
        self.WriteSection(f, 'Fermentation Summary')

        self.WriteArg(f, 'Actual OG', NumString(self.actualOG,'Gravity'))
        self.WriteArg(f, 'Actual FG', NumString(self.actualFG,'Gravity'))
        self.WriteArg(f, 'Actual Color', str(self.actualColor),'\n')
        
        f.write('  Yeast:               '+self.yeast.name+'\n\n')
        
        f.write('  Fermentables List:\n')
        
        for ferm in self.fermentables:
            self.WriteFermentable(f,ferm)
        
        self.WriteSection(f, 'Hops Summary')
        self.WriteArg(f, 'Hop Formula', self.hopFormulaName, '\n')

        f.write('  Hops List:\n')
        
        for hop in self.hops:
            self.WriteHop(f,hop)
        
        if self.otherIngredients:
            self.WriteSection(f, 'Other Ingredients')

            for other in self.otherIngredients:
                self.WriteOther(f,other)
                          
        self.WriteSection(f, 'Notes')
        f.write(self.notes)
        
        
        f.close()
        
               
                    
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
            self.totalIBU += hop.calcIBU(self.hopFormulaName, totalSize, 
                                         self.boilSize, self.calcOG)

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
    def calcCalories(self, ABW, OG, FG):
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
                self.hops == other.hops and
                self.hopFormulaName == other.hopFormulaName)

    #----------------------------------------------------------------------
    def __ne__(self, other):
        """ Inequality definition for a project """
        return not self.__eq__(other)
