
import csv
from pyBrew.pyBrewMethods import GetFloat

###############################################################################
class FermDb(object):
    grainDict = {}
    try:
        dbFile = csv.reader(open('pyBrew/Databases/grains.csv', 'r'))
        dbFile.next() #Skip header row
        for name, pot, srm, max, eff in dbFile:
            grainDict[name] = {'Potential': GetFloat(pot),
                               'SRM': GetFloat(srm),
                               'Max': GetFloat(max),
                               'Efficiency': GetFloat(eff)}
            
    except (IOError, ValueError):
        print "ERROR: Unable to load grains database"
        
        
    Names = sorted(grainDict.keys(), key=str.lower)

    #----------------------------------------------------------------------
    @classmethod
    def GetID(cls, fermName):
        try:
            return cls.Names.index(fermName)
        except ValueError:
            return -1

    #----------------------------------------------------------------------
    @classmethod
    def Potential(cls, fermName):
        try:
            return cls.grainDict[fermName]['Potential']
        except KeyError:
            return 0.
    
    #----------------------------------------------------------------------
    @classmethod
    def Efficiency(cls, fermName):
        try:
            efficiency = cls.grainDict[fermName]['Efficiency']
        except KeyError:
            efficiency = 100.
        return efficiency
        
    #----------------------------------------------------------------------
    @classmethod
    def SRM(cls, fermName):
        try:
            SRM = cls.grainDict[fermName]['SRM']
        except KeyError:
            SRM = 0.
        return SRM
        
    #----------------------------------------------------------------------
    @classmethod
    def Max(cls, fermName):
        try:
            max = cls.grainDict[fermName]['Max']
        except KeyError:
            max = 100.
        return max
    