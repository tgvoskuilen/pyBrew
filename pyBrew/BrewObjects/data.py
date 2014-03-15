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
import os

from project import Project
from recipe import Recipe

###############################################################################
class Data(object):
    """
    Main data class object, holds a list of projects and a list of recipes
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """
        Look in data folder and get all project and recipe files. Initialize
        all projects and recipes from these files. Since there must always
        be at least one of each, if none are found, make a new one.
        """
        
        # TODO: Allow user to change default data folder location 
        # (to put on dropbox or elsewhere)
        self.folder = os.path.join(os.path.expanduser('~'),'pyBrew')
        
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
            
        items = os.listdir(self.folder)
        
        projfiles = [f for f in items if f.endswith('.proj')]
        recipefiles = [f for f in items if f.endswith('.recip')]
        
        self.projects = []
        self.recipes = []
        
        if projfiles:
            for proj in projfiles:
                self.projects.append( Project(folder=self.folder, filename=proj) )
        else:
            # TODO: Can we make this requirement go away?
            self.projects.append( Project(folder=self.folder, name='New Project') )
            
        if recipefiles:
            for recipe in recipefiles:
                self.recipes.append( Recipe(folder=self.folder, filename=recipe) )
        else:
            # TODO: Can we make this requirement go away?
            self.recipes.append( Recipe(folder=self.folder, name='New Recipe') )
            
    #----------------------------------------------------------------------   
    def AddProject(self,projectName):
        """ Add a new project """
        self.projects.append( Project(folder=self.folder, name=projectName) )
        
    #----------------------------------------------------------------------   
    def AddRecipe(self,recipeName):
        """ Add a new recipe """
        self.recipes.append( Recipe(folder=self.folder, name=recipeName) )
          
    #----------------------------------------------------------------------
    def getProjectNames(self):
        """ Get a list of all project names """
        return [project.name for project in self.projects]
        
    #----------------------------------------------------------------------
    def getRecipeNames(self):
        """ Get a list of all recipe names """
        return [recipe.name for recipe in self.recipes]

    #----------------------------------------------------------------------
    def Save(self):
        """ Call Save() on each project and recipe """
        for project in self.projects:
            project.Save()
            
        for recipe in self.recipes:
            recipe.Save()
            
            
