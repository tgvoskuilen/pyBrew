
import csv
from pyBrew.pyBrewMethods import GetFloat
from pyBrew.range import Range

###############################################################################
class YeastDb(object):
    yeastDict = {}
    try:
        dbFile = csv.reader(open('pyBrew/Databases/yeasts.csv', 'r'))
        dbFile.next() #Skip header row
        for name, attenL, attenH, floc, tempL, tempH, desc in dbFile:
            yeastDict[name] = {'Attenuation': (GetFloat(attenL, -1),
                                               GetFloat(attenH, -1)),
                               'Temperature': (GetFloat(tempL, -1), 
                                               GetFloat(tempH, -1)),
                               'Description': desc,
                               'Flocculation': floc}
    except (IOError, ValueError):
        print "ERROR: Unable to load yeasts database"
        

    Names = sorted(yeastDict.keys(), key=str.lower)
    
    #----------------------------------------------------------------------
    @classmethod
    def AttenRange(cls, yeastName):
        try:
            attenuation = cls.yeastDict[yeastName]['Attenuation']
        except KeyError:
            attenuation = (0.,0.)
        return Range(attenuation, True)
        
    #----------------------------------------------------------------------
    @classmethod
    def Attenuation(cls, yeastName):
        try:
            attenuation = cls.yeastDict[yeastName]['Attenuation']
        except KeyError:
            attenuation = (0.,0.)
        return attenuation[0]
        
    #----------------------------------------------------------------------
    @classmethod
    def Description(cls, yeastName):
        try:
            description = cls.yeastDict[yeastName]['Description']
            description += cls.FermTemp(yeastName)
            description += cls.Flocculation(yeastName)
        except KeyError:
            description = ''
        return description
        
    #----------------------------------------------------------------------
    @classmethod
    def FermTemp(cls, yeastName):
        try:
            fermTemps = cls.yeastDict[yeastName]['Temperature']
            if fermTemps[0] > 0:
                ftstr='\n\nFermentation temperature: %2.0f - %2.0f F'%fermTemps
            else:
                ftstr = ''
        except KeyError:
            ftstr = ''
        return ftstr
    
    #----------------------------------------------------------------------
    @classmethod
    def Flocculation(cls, yeastName):
        try:
            flocstr = cls.yeastDict[yeastName]['Flocculation']
            if flocstr != '' and flocstr != ' ':
                flout = '\n\nFlocculation: %s' % flocstr
            else:
                flout = ''
        except KeyError:
            flout = ''
        return flout
    
    #----------------------------------------------------------------------
    @classmethod
    def GetID(cls, yeastName):
        try:
            yeast_id = cls.Names.index(yeastName)
        except ValueError:
            yeast_id = -1
        return yeast_id
