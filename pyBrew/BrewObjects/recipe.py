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
import os

from fermentable import Fermentable
from hop import Hop
from other import Other
from yeast import Yeast
from quantity import Quantity
from brewfile import BrewFile

from pyBrew.pyBrewMethods import GetFloat
from pyBrew.pyBrewMethods import NumString
from pyBrew.pyBrewMethods import ReadLine

###############################################################################
class Recipe(BrewFile):
    """
    This class contains the data saved for each recipe.
    """
    #----------------------------------------------------------------------
    def __init__(self, folder, name=None, filename=None):
        
        
        self.fermentables = []
        self.hops = []
        self.yeasts = []
        self.otherIngredients = []
        self.batchSize = 0.
        self.targetOG = 0.
        self.description = 'Add a description'
        self.instructions = 'Add instructions'
        
        BrewFile.__init__(self, folder, 'recip', name, filename)
        

            
            
    #----------------------------------------------------------------------    
    def ReadFile(self):
        
        try:
            lines = self.GetLines()
            self.name = self.GetTitle(lines)
 
            self.CheckName()
            
            sections = self.GetSections(lines)
                
            #Load section by section
            if "Recipe Summary" in sections:
                for line in sections['Recipe Summary']:
                
                    if 'recipe size' in line.lower():
                        amt, unit = ReadLine(line.lower(), "recipe size")
                        self.batchSize = GetFloat(amt) #TODO Use Quantity()
                        
                    if 'Target OG' in line:
                        amt, unit = ReadLine(line, "Target OG")
                        self.targetOG = GetFloat(amt)
                            
                
            if "Description" in sections:
                self.description = ''.join(sections['Description'])
                
            if "Instructions" in sections:
                self.description = ''.join(sections['Instructions'])
                
            if "Ingredients" in sections:
                reading ={'Hops':False, 
                          'Fermentables':False, 
                          'Yeasts':False, 
                          'Other':False}
                          
                for line in sections['Ingredients']:
                
                    for key in reading:
                        if reading[key] and not line.strip():
                            reading[key] = False
                            break
                            
                    if reading['Hops']:
                        self.hops.append( self.ReadHop(line) )
                    
                    if reading['Fermentables']:
                        self.fermentables.append( self.ReadFermentable(line) )
                        
                    if reading['Yeasts']:
                        self.yeasts.append( self.ReadYeast(line) )
                    
                    if reading['Other']:
                        self.otherIngredients.append( self.ReadOther(line) )
                    
                    
                    if 'Hops List' in line:
                        reading['Hops'] = True
                        
                    if 'Fermentables List' in line:
                        reading['Fermentables'] = True
                        
                    if 'Yeast List' in line:
                        reading['Yeasts'] = True
                        
                    if 'Other Ingredients' in line:
                        reading['Other'] = True
                
                
            return True
            
        except IOError:
            return False

    #----------------------------------------------------------------------    
    def WriteFile(self):
        f = open(self.path, 'w')
        self.WriteHeader(f)
        
        self.WriteSection(f,'Recipe Summary')
        self.WriteArg(f, 'Recipe size', str(self.batchSize), 'gallons')
        self.WriteArg(f, 'Target OG', NumString(self.targetOG,'Gravity')) 
        
        self.WriteSection(f,'\nDescription')
        f.write(self.description)
        
        self.WriteSection(f,'\nInstructions')
        f.write(self.instructions)
        
        self.WriteSection(f,'\nIngredients')
        
        f.write('\n  Fermentables List:\n')
        for ferm in self.fermentables:
            self.WriteFermentable(f,ferm)
            
        f.write('\n  Hops List:\n')
        for hop in self.hops:
            self.WriteHop(f,hop)
            
        f.write('\n  Yeast List:\n')
        for yeast in self.yeasts:
            f.write('    '+yeast.name+'\n')
            
        if self.otherIngredients:
            f.write('\n  Other Ingredients:\n')
            for other in self.otherIngredients:
                self.WriteOther(f,other)
              
    #----------------------------------------------------------------------
    def Scale(self, scale_factor):
        self.batchSize *= scale_factor
        for ferm in self.fermentables:
            ferm.amount.Scale(scale_factor)
        for hop in self.hops:
            hop.amount.Scale(scale_factor)
        for other in self.otherIngredients:
            other.amount.Scale(scale_factor)
    
    #----------------------------------------------------------------------
    def Export(self, filename=None):
        if filename is None:
                filename = os.getcwd() + '/' + self.name
                
        recipeFile = csv.writer(open(filename, 'w'))
        recipeFile.writerow(['Recipe Name', self.name])
        recipeFile.writerow(['Batch Size', str(self.batchSize)])
        recipeFile.writerow(['Target OG', str(self.targetOG)])
        recipeFile.writerow(['Description',  self.description])
        recipeFile.writerow(['Instructions', self.instructions])
        
        recipeFile.writerow(['Fermentables', str(len(self.fermentables))])
        for ferm in self.fermentables:
            recipeFile.writerow([ferm.name, str(ferm.amount.Value()), ferm.amount.Unit()])
            
        recipeFile.writerow(['Hops', str(len(self.hops))])
        for hop in self.hops:
            recipeFile.writerow([hop.name, str(hop.amount.Value()), hop.amount.Unit()])
        
        recipeFile.writerow(['Yeast', str(len(self.yeasts))])
        for yeast in self.yeasts:
            recipeFile.writerow([yeast.name])
        
        recipeFile.writerow(['Other Ingredients', str(len(self.otherIngredients))])
        for other in self.otherIngredients:
            recipeFile.writerow([other.name, str(other.amount.Value()), other.amount.Unit()])
        
    #----------------------------------------------------------------------
    def Import(self, filename):
        try:
            recipeFile = csv.reader(open(filename, 'r'))
            fileData = []
            for row in recipeFile:
                fileData.append(row)
                
            #Extract data to recipe
            self.name = fileData[0][1]
            self.batchSize = GetFloat(fileData[1][1])
            self.targetOG = GetFloat(fileData[2][1])
            self.description = fileData[3][1]
            self.instructions = fileData[4][1]

            fRow = 6
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
            for y in range(yRow, yRow + ny):
                self.yeasts.append(Yeast(fileData[y][0]))
            
            oRow = yRow + ny + 1
            no = int(fileData[oRow-1][1])
            for o in range(oRow, oRow + no):
                self.otherIngredients.append(Other(fileData[o][0],
                                            Quantity(GetFloat(fileData[o][1]),
                                            fileData[o][2])))
                
            return True
        except:
            return False
        
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """ Equality definition for a recipe """
        return (self.name == other.name and
                self.batchSize == other.batchSize and
                self.targetOG == other.targetOG and
                self.description == other.description and
                self.instructions == other.instructions and
                self.yeasts == other.yeasts and
                self.fermentables == other.fermentables and
                self.hops == other.hops and
                self.otherIngredients == other.otherIngredients)

    #----------------------------------------------------------------------
    def __ne__(self, other):
        """ Inequality definition for a recipe """
        return not self.__eq__(other)
