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

import pickle

from projectData import Project
from recipeData import Recipe

###############################################################################
class RootData(object):
    """
    Main data class object, saves and manages all user data
    """
    #----------------------------------------------------------------------
    @classmethod
    def Load(cls, filename='mydata.brew'):
        try:
            data = pickle.load(open('UserData/'+filename, 'rb'))
        except IOError:
            data = RootData()
            pickle.dump(data, open('UserData/'+filename, 'wb'), -1)
        return data
        
    #----------------------------------------------------------------------
    def __init__(self):
        self.projects = [Project()]
        self.recipes = [Recipe()]

    #----------------------------------------------------------------------
    def getProjectNames(self):
        return [project.name for project in self.projects]
        
    #----------------------------------------------------------------------
    def getRecipeNames(self):
        return [recipe.name for recipe in self.recipes]

    #----------------------------------------------------------------------
    def Save(self):
        pass #TODO
