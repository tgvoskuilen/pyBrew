import math
import pyBrew.Databases
from pyBrew.range import Range
from pyBrew.pyBrewMethods import Mean

###############################################################################
class Style(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, name=''):
        
        if pyBrew.Databases.StyleDb.IsValid(name):
            self.name = name
            self.SRM= Range(pyBrew.Databases.StyleDb.GetParam(name,'SRM'),True)
            self.IBU= Range(pyBrew.Databases.StyleDb.GetParam(name,'IBU'),True)
            self.OG = Range(pyBrew.Databases.StyleDb.GetParam(name,'OG'), True)
            self.FG = Range(pyBrew.Databases.StyleDb.GetParam(name,'FG'), True)
            
            
            self.attenuation = 100. * (1. - (self.FG-1.)/(self.OG-1.))
            self.ABW = 76.08 * (self.OG - self.FG)/(1.775 - self.OG)
            self.ABV = self.ABW * self.FG / 0.794
            PO = 0.1808*(668.72*self.OG-463.37-205.25*self.OG**2.)
            PF = 0.8192*(668.72*self.FG-463.37-205.25*self.FG**2.)
            self.calories = ((6.9*self.ABW + 4.*((PO + PF) - 0.1)) * 
                              self.FG * 3.55 * 16. / 12.)
        else:
            self.name = ''
            self.SRM = Range((0,0))
            self.IBU = Range((0,0))
            self.OG = Range((0,0))
            self.FG = Range((0,0))
            self.attenuation = Range((0,0))
            self.ABV = Range((0,0))
            self.ABW = Range((0,0))
            self.calories = Range((0,0))

    #----------------------------------------------------------------------
    def __eq__(self, other):
        """ Define the style equality operator """
        return self.name == other.name

    #----------------------------------------------------------------------
    def __ne__(self, other):
        """ Define the style inequality operator """
        return not self.__eq__(other)