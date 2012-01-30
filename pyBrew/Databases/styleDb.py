
import csv
from pyBrew.pyBrewMethods import GetFloat

###############################################################################
class StyleDb(object):
    styleDict = {}
    try:
        dbFile = csv.reader(open('pyBrew/Databases/styles.csv', 'r'))
        dbFile.next() #Skip header row
        for name, cat, OGL, OGH, FGL, FGH, ABVL, \
            ABVH, IBUL, IBUH, SRML, SRMH, source in dbFile:
            styleDict[name] = {'OG':  (GetFloat(OGL,-1),  GetFloat(OGH,-1)),
                               'FG':  (GetFloat(FGL,-1),  GetFloat(FGH,-1)),
                               'ABV': (GetFloat(ABVL,-1), GetFloat(ABVH,-1)),
                               'SRM': (GetFloat(SRML,-1), GetFloat(SRMH,-1)),
                               'IBU': (GetFloat(IBUL,-1), GetFloat(IBUH,-1)),
                               'Category': cat,
                               'Source': source}
            
    except (IOError, ValueError):
        print "ERROR: Unable to load styles database"


    #Use styleDict to get name lists and IDs
    styleCat = {}
    for style, db in styleDict.iteritems():
        styleCat.setdefault(db['Category'],[]).append(style)

    for styleName, styleList in styleCat.iteritems():
        styleCat[styleName] = sorted(styleList)
        
    styleNames = []
    styleLookup = []

    for category in enumerate(styleCat):
        styleNames.append('--'+category[1]+'--')
        styleLookup.append('NA')
        for style in styleCat[category[1]]:
            styleNames.append(style)
            styleLookup.append(style)
        styleNames.append('')
        styleLookup.append('NA')
        
    try:
        styleNames.pop()
        styleLookup.pop()
    except IndexError:
        pass
        
    #----------------------------------------------------------------------
    @classmethod
    def GetNameList(cls):
        return cls.styleNames
        
    #----------------------------------------------------------------------
    @classmethod
    def GetID(cls, styleName):
        try:
            style_id = cls.styleLookup.index(styleName)
        except ValueError:
            style_id = -1
        return style_id
        
    #----------------------------------------------------------------------
    @classmethod
    def IsValid(cls, styleName):
        try:
            style_id = cls.styleLookup.index(styleName)
        except ValueError:
            style_id = -1
        return (style_id >= 0)
        
    #----------------------------------------------------------------------
    @classmethod
    def GetParam(cls, styleName, param):
        return cls.styleDict[styleName][param]