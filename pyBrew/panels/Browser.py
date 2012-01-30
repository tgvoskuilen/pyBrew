
import wx

###############################################################################
class BlankPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        txt = wx.StaticText(self,-1,'Select a project or recipe...')


###############################################################################
class RecipePanel(wx.Panel):
    """
    
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.txtWidth = 250
        
        #Items
        self.title=wx.StaticText(self,-1,'')
        headerFont = wx.Font(pointSize=11,
                             family=wx.FONTFAMILY_DEFAULT,
                             weight=wx.FONTWEIGHT_BOLD,
                             style=wx.FONTSTYLE_NORMAL)
        self.title.SetFont(headerFont)
        
        self.description = wx.StaticText(self,-1,'')
                
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.title, 0, wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((10,-1))
        hBoxes[-1].Add(self.description, 1, wx.EXPAND|wx.ALL, 5)
        
        for hBox in hBoxes:
            vBox.Add(hBox, 0, wx.ALL, 5)
        
        self.SetSizer(vBox)
        
    def SetValues(self, recipeID):
        self.title.SetLabel(self.parent.data.recipes[recipeID].name)
        self.description.SetLabel(self.parent.data.recipes[recipeID].description)
        self.description.Wrap(self.txtWidth)
        
###############################################################################
class ProjectPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        
        #Items
        self.title=wx.StaticText(self,-1,'')
        headerFont = wx.Font(pointSize=11,
                             family=wx.FONTFAMILY_DEFAULT,
                             weight=wx.FONTWEIGHT_BOLD,
                             style=wx.FONTSTYLE_NORMAL)
        self.title.SetFont(headerFont)
        
        self.brewDate = wx.StaticText(self,-1,'')
        self.IBU = wx.StaticText(self,-1,'')
        self.ABV = wx.StaticText(self,-1,'')
        self.fermTime = wx.StaticText(self,-1,'')
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.title, 0, wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((10,-1))
        hBoxes[-1].Add(self.brewDate, 1, wx.EXPAND|wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((10,-1))
        hBoxes[-1].Add(self.IBU, 1, wx.EXPAND|wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((10,-1))
        hBoxes[-1].Add(self.ABV, 1, wx.EXPAND|wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((10,-1))
        hBoxes[-1].Add(self.fermTime, 1, wx.EXPAND|wx.ALL, 5)
        
        for hBox in hBoxes:
            vBox.Add(hBox, 0, wx.ALL, 5)
        
        self.SetSizer(vBox)
        
    #----------------------------------------------------------------------
    def SetValues(self, projID):
        self.title.SetLabel(self.parent.data.projects[projID].name)
        brewstr = 'Brewed on '+self.parent.data.projects[projID].brewDate
        self.brewDate.SetLabel(brewstr)
        self.parent.data.projects[projID].CalcValues()
        IBUstr = 'IBU of '+'%2.0f'%self.parent.data.projects[projID].totalIBU
        self.IBU.SetLabel(IBUstr)
        ABVstr = 'Alcohol content of '+ \
            str(self.parent.data.projects[projID].calcABV) + ' %'
        self.ABV.SetLabel(ABVstr)
        fermTimestr = 'Fermentation time of %2.0f days' % \
                    (self.parent.data.projects[projID].daysInPrimary+\
                     self.parent.data.projects[projID].daysInSecondary)
        self.fermTime.SetLabel(fermTimestr)
        

###############################################################################
class Browser(wx.Panel):
    """
    This is the main project panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, name='browser')
        
        self.parent = parent
        self.data = self.parent.parent.data
        
        #display panels
        self.blankPanel = BlankPanel(self)
        self.recipePanel = RecipePanel(self)
        self.projectPanel = ProjectPanel(self)
        
        self.recipePanel.Hide()
        self.projectPanel.Hide()
        
        #Spacer box
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        headerFont = wx.Font(pointSize=11,
                             family=wx.FONTFAMILY_DEFAULT,
                             weight=wx.FONTWEIGHT_BOLD,
                             style=wx.FONTSTYLE_NORMAL)
                             
        #title = wx.StaticText(self, -1, "Home")
        
        self.tree = wx.TreeCtrl(self, style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|
                                wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
                                
        self.root = self.tree.AddRoot('Database')
        self.projects = self.tree.AppendItem(self.root, 'Projects')
        self.recipes = self.tree.AppendItem(self.root, 'Recipes')
        self.tree.SetFont(headerFont)
        
        hBox.Add(self.blankPanel, 1, wx.EXPAND|wx.ALL, 10)
        hBox.Add(self.recipePanel, 1, wx.EXPAND|wx.ALL, 10)
        hBox.Add(self.projectPanel, 1, wx.EXPAND|wx.ALL, 10)
        hBox.Add(self.tree, 1, wx.EXPAND|wx.ALL, 10)
        
        self.SetSizer(hBox)
        
        #Bind double-click or enter to load selected item
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.loadItem, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.changePanel, self.tree)
        
        self.LoadActivePanel()
        
    #----------------------------------------------------------------------
    def changePanel(self, event):
        item = event.GetItem()
        par = self.tree.GetItemParent(item)
        if par == self.projects:
            if self.blankPanel.IsShown(): self.blankPanel.Hide()
            elif self.recipePanel.IsShown(): self.recipePanel.Hide()
            self.projectPanel.Show()
            ID=self.data.getProjectNames().index(self.tree.GetItemText(item))
            self.projectPanel.SetValues(ID)
        elif par == self.recipes:
            if self.blankPanel.IsShown(): self.blankPanel.Hide()
            elif self.projectPanel.IsShown(): self.projectPanel.Hide()
            self.recipePanel.Show()
            ID=self.data.getRecipeNames().index(self.tree.GetItemText(item))
            self.recipePanel.SetValues(ID)
        else:
            if self.recipePanel.IsShown(): self.recipePanel.Hide()
            elif self.projectPanel.IsShown(): self.projectPanel.Hide()
            self.blankPanel.Show()
        self.Layout()
        
    #----------------------------------------------------------------------
    def loadItem(self, event):
        item = event.GetItem()
        par = self.tree.GetItemParent(item)
        if par == self.projects:
            ID=self.data.getProjectNames().index(self.tree.GetItemText(item))
            self.parent.SetToProjects(ID)
        elif par == self.recipes:
            ID=self.data.getRecipeNames().index(self.tree.GetItemText(item))
            self.parent.SetToRecipes(ID)
        else:
            event.Skip()

            
    #----------------------------------------------------------------------
    def LoadActivePanel(self):
        #print "Load data in Panels.Browser"
        self.tree.DeleteChildren(self.projects)
        self.tree.DeleteChildren(self.recipes)
        projectNames = self.data.getProjectNames()
        recipeNames = self.data.getRecipeNames()
        
        #Projects and Recipes to tree
        for project in projectNames:
            self.tree.AppendItem(self.projects, project)
            
        for recipe in recipeNames:
            self.tree.AppendItem(self.recipes, recipe)
            
        self.tree.SetItemHasChildren(self.projects, len(projectNames)>0)
        self.tree.SetItemHasChildren(self.recipes, len(recipeNames)>0)
        self.tree.ExpandAll()