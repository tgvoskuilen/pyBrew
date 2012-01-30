
import csv
from pyBrew.pyBrewMethods import GetFloat

###############################################################################
class HopDb(object):
    hopDict = {}
    try:
        dbFile = csv.reader(open('pyBrew/Databases/hops.csv', 'r'))
        dbFile.next() #Skip header row
        for name, aau in dbFile:
            hopDict[name] = {'AAU': GetFloat(aau)}
            
    except (IOError, ValueError):
        print "ERROR: Unable to load hops database"
        
    Names = sorted(hopDict.keys(), key=str.lower)
    
    FormulaNames = ['Tinseth','Rager','Daniels','Garetz']
    Forms = ['Pellets', 'Whole']
    
        
    #----------------------------------------------------------------------
    @classmethod
    def GetID(cls, hopName):
        try:
            hop_id = cls.Names.index(hopName)
        except ValueError:
            hop_id = -1
        return hop_id
        
    #----------------------------------------------------------------------
    @classmethod
    def AAU(cls, hopName):
        try:
            return cls.hopDict[hopName]['AAU']
        except KeyError:
            return 0.