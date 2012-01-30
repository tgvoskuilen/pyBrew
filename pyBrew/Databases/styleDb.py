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
