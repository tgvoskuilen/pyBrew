
import pyBrew.Databases

###############################################################################
class Yeast(object):
    """ Class to describe yeasts and their properties """
    #----------------------------------------------------------------------
    def __init__(self, name=''):
        self.name = name
        #self.attenuation = pyBrew.Databases.YeastDb.Attenuation(self.name)
        self.attenuation = pyBrew.Databases.YeastDb.AttenRange(self.name)
        
    #----------------------------------------------------------------------
    def GetColStrings(self):
        return ['1 packet']
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """ Define the yeast equality operator """
        return self.name == other.name

    #----------------------------------------------------------------------
    def __ne__(self, other):
        """ Define the yeast inequality operator """
        return not self.__eq__(other)