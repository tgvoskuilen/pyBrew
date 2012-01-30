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
