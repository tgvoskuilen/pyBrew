
import pyBrew.Databases

###############################################################################
# Fermentable - Class for each fermentable object
#
###############################################################################
class Fermentable(object):
    """ Class to define each fermentable item """
    #-------------------------------------------------------------------------
    def __init__(self, name, quantity):
        self.name = name
        self.amount = quantity

        #Get properties from the database
        self.potential = pyBrew.Databases.FermDb.Potential(self.name)
        self.efficiency = pyBrew.Databases.FermDb.Efficiency(self.name)
        self.SRM = pyBrew.Databases.FermDb.SRM(self.name)
        self.Max = pyBrew.Databases.FermDb.Max(self.name) #TODO Warn if this is exceeded
        
        #Calculated parameters
        self.gravity = 1.
        self.percent = 0
        self.color = 0


    #-------------------------------------------------------------------------
    def GetColStrings(self):
        return [str(self.amount.Value())+'  '+self.amount.UnitShort(),
                '%4.3f' % self.potential,
                '%4.3f' % self.gravity,
                '%3.0f' % self.percent,
                '%2.0f' % self.color]
        
    #-------------------------------------------------------------------------
    def calcGravity(self, totalSize, batchSize):
        """ Calculate the gravity contribution of a grain to the boil """
        if batchSize > 0.:
            if totalSize > 0.:
                self.gravity = round((self.potential - 1.) * 
                                     self.amount.Value('pounds')/totalSize * 
                                     self.efficiency/100. + 1., 3)
            else:
                self.gravity = 1.
            return self.gravity - 1.
        else:
            self.gravity = 1.
            return 0.

    #-------------------------------------------------------------------------
    def calcPercent(self, OG):
        """ Calculate the percent of the gravity from this fermentable """
        if OG > 1.:
            self.percent = round( (self.gravity - 1.)*100. / (OG - 1.) )
        else:
            self.percent = 0

    #-------------------------------------------------------------------------
    def calcColor(self, totalSize, batchSize):
        """ Calculate the color due to this fermentable """
        if totalSize > 0. and batchSize > 0.:
            self.color = round( self.amount.Value('pounds') * 
                                self.SRM / totalSize )
        else:
            self.color = 0
        return self.color

    #-------------------------------------------------------------------------
    def __eq__(self, other):
        """ Define the fermentables equality operator """
        #Check each item. If any are unequal, return false
        return (self.name == other.name and
                self.amount == other.amount)

    #-------------------------------------------------------------------------
    def __ne__(self, other):
        """ Define the fermentables inequality operator """
        return not self.__eq__(other)