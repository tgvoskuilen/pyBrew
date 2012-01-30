
from fermData import Fermentable
from hopData import Hop
from otherData import Other
from yeastData import Yeast
from quantity import Quantity

import os
from pyBrew.pyBrewMethods import GetFloat

###############################################################################
class Recipe(object):
    """
    This class contains the data saved for each recipe.
    """
    #----------------------------------------------------------------------
    def __init__(self, name='New Recipe'):
        self.name = name
        self.batchSize = 0.
        self.targetOG = 0.
        self.description = 'Add a description'
        self.instructions = 'Add instructions'
        self.fermentables = []
        self.hops = []
        self.yeasts = []
        self.otherIngredients = []
        
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