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
    
