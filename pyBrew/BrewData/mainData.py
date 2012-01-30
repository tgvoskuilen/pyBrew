
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