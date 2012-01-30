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
