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

import re
import os

from fermentable import Fermentable
from hop import Hop
from other import Other
from yeast import Yeast
from quantity import Quantity

from pyBrew.pyBrewMethods import GetFloat

###############################################################################
class BrewFile(object):
    """
    This class manages files for both projects and recipes. Both project
    and recipe are derived from this class.
    
    What is path?
      - The full path to an existing data file
      - Partial path to a proposed data file (dataFolder/filename) with no
        extension. What if the user types the extension??
    """
    #----------------------------------------------------------------------
    def __init__(self, path, ext):
        
        self.ext = ext
        self.hasChanged = False
        
        
        if self.FileExists(path):
            # If path was the full path to the file, just use directly
            self.path = path
            self.name = '' #Using no name triggers read in Project and Recipe
        else:
            # Input is a new project, make sure there are no name conflicts
            
            self.path = path+'.'+ext
            
            if os.path.isfile(self.path):
                i = 1
                while i < 100:
                    newpath = path+' ('+str(i)+').'+ext
                    if not os.path.isfile(newpath):
                        self.path = newpath
                        break
                    i += 1
                    
            self.name = os.path.split(path)[1]
        
    
    #----------------------------------------------------------------------   
    def FileExists(self,path):
        return os.path.isfile(path) and path.endswith('.'+self.ext)
        
        
    #----------------------------------------------------------------------   
    def Save(self):
        if self.hasChanged:
            basename = os.path.split(self.path)[1]
            if basename.split('.'+self.ext)[0] != self.name:
                self.RenameFile()
                
            self.WriteFile()
            self.hasChanged = False
            
            
    #----------------------------------------------------------------------    
    def DeleteFile(self):
        if os.path.isfile(self.path):
            os.remove(self.path)
            
    #----------------------------------------------------------------------     
    def RenameFile(self):
        """
        Rename the file to match its name
        """
        parts = os.path.split(self.path)
        newname = os.path.join(parts[0],self.name+'.'+self.ext)
        if not os.path.isfile(newname):
            os.rename(self.path, newname)
            self.path = newname
            
        else:
            i = 1
            while i < 100:
                newname = os.path.join(parts[0],self.name+' ('+str(i)+').'+self.ext)
                if not os.path.isfile(newname):
                    os.rename(self.path, newname)
                    self.path = newname
                    self.name += ' ('+str(i)+')'
                    break
                else:
                    i += 1
        
    #----------------------------------------------------------------------     
    def GetLines(self):
        f = open(self.path, 'r')
        lines = f.readlines()
        f.close()
        return lines
        
    #----------------------------------------------------------------------     
    def GetTitle(self,lines):
        #Extract title from line 2
        getTitle = re.search(r'\* (.*) \*', lines[1]) 
        return getTitle.group(1).strip()

    #----------------------------------------------------------------------    
    def CheckName(self):
        #If title and filename do not match, change filename
        basename = os.path.split(self.path)[1]
        if basename.split('.'+self.ext)[0] != self.name:
            self.RenameFile()
            
            
    #----------------------------------------------------------------------    
    def GetSections(self,lines):
        #Read sections from file
        sections = {}
        secStart = -1
        secEnd = -1
        lastTitle = ''
        for i,line in enumerate(lines):
            if line[0:5] == 5*'-':
                secTitle = lines[i-1].strip()
                sections[secTitle] = [i+1]

                if lastTitle:
                    sections[lastTitle].append(i-2)

                lastTitle = secTitle

        #load lines into each section
        for s,idx in sections.iteritems():
            if len(sections[s]) == 1:
                secLines = lines[idx[0]:len(lines)]
            else:
                secLines = lines[idx[0]:idx[1]]

            sections[s] = secLines
        return sections
        
    #----------------------------------------------------------------------    
    def ReadHop(self,line):
        spl = line.split('(')
        seg1 = spl[0].strip()
        seg2 = spl[1].split(')')[0].strip()
        
        splA = seg1.split(' ')
        getParam = re.search(r'(.*) min, (.*)% AAU, (.*)',seg2)
        
        name = ' '.join(splA[0:len(splA)-2]).strip()
        amt = float(splA[len(splA)-2].strip())
        unit = splA[len(splA)-1].strip()
        time = GetFloat(getParam.group(1).strip())
        aau = GetFloat(getParam.group(2).strip())
        form = getParam.group(3).strip()
        
        return Hop(name, Quantity(amt, unit), time, aau, form)
        
    #----------------------------------------------------------------------    
    def ReadFermentable(self,line):
        spl = line.split(' ')
        name = ' '.join(spl[0:len(spl)-2]).strip()
        amt = float(spl[len(spl)-2].strip())
        unit = spl[len(spl)-1].strip()
        
        return Fermentable(name, Quantity(amt, unit)) 

    #----------------------------------------------------------------------    
    def ReadYeast(self,line):
        return Yeast(line.strip())
     
    #----------------------------------------------------------------------    
    def ReadOther(self,line):
        spl = line.split(' ')
        name = ' '.join(spl[0:len(spl)-2]).strip()
        amt = float(spl[len(spl)-2].strip())
        unit = spl[len(spl)-1].strip()
        
        return Other(name, Quantity(amt, unit)) 

    #----------------------------------------------------------------------    
    def WriteHop(self,f,hop):
        f.write('    '+hop.name+' '*(15-len(hop.name))+' '
                       +str(hop.amount.Value())+' '+hop.amount.Unit()
                       +' ('+str(hop.boiltime)+' min, '
                       +str(hop.aau)+'% AAU, '+hop.form+')\n')
                       
    #----------------------------------------------------------------------    
    def WriteFermentable(self,f,fermentable):  
        f.write('    '+fermentable.name+' '*(30-len(fermentable.name))+' '
                  + str(fermentable.amount.Value()) + ' ' 
                  + fermentable.amount.Unit() + '\n')
      
    #----------------------------------------------------------------------    
    def WriteOther(self,f,other):  
        f.write('    '+other.name+' '*(35-len(other.name))+' '
                      +str(other.amount.Value())+' '
                      +other.amount.Unit()+'\n')
                      
    #----------------------------------------------------------------------    
    def WriteArg(self, f, argname, value, unit=''): 
        s = '  '+argname+':'+' '*(20-len(argname))+' '+value+' '+unit+'\n';
        f.write(s)
    
    #----------------------------------------------------------------------    
    def WriteSection(self, f, title): 
        f.write('\n'+title+'\n'+'-'*79+'\n')
     
    #----------------------------------------------------------------------    
    def WriteHeader(self, f): 
        f.write('*'*79+'\n')
        f.write('* '+ self.name + ' '*(76-len(self.name)) + '*\n')
        f.write('*'*79+'\n\n')
