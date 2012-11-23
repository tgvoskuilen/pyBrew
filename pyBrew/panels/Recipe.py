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

import wx
import pickle

import pyBrew.dialogs
from pyBrew.pyBrewMethods import NumString
from pyBrew.pyBrewMethods import GetFloat

###############################################################################
class Main(wx.Panel):
    """
    This is the main project panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        
        #Grab the root data object
        self.data = parent.parent.parent.data
        
        #Define header font
        headerFont = wx.Font(pointSize=12,
                             family=wx.FONTFAMILY_DEFAULT,
                             weight=wx.FONTWEIGHT_BOLD,
                             style=wx.FONTSTYLE_NORMAL)

        #Create all editable/controllable items
        self.recipeSelection = wx.ComboBox(self, -1, style=wx.CB_READONLY)
        self.name            = wx.TextCtrl(self, -1)
        self.description     = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.batchSize       = wx.TextCtrl(self, -1, size=(100,-1))
        self.targetOG        = wx.TextCtrl(self, -1, size=(100,-1))
        self.save            = wx.Button(self, wx.ID_SAVE, 'Save Changes')
        self.save.Enable(False)
        
        selectLabel   =wx.StaticText(self, -1, 'Select Recipe')
        selectLabel.SetFont(headerFont)
        maxSize       =selectLabel.GetSize()
        labSize       =(maxSize[0],-1)
        nameLabel     =wx.StaticText(self,-1,'Recipe Name',size=labSize)
        descLabel     =wx.StaticText(self,-1,'Description',size=labSize)
        batchSizeLabel=wx.StaticText(self,-1,'Recipe Size (gal)',size=labSize)
        targetOGLabel =wx.StaticText(self,-1,'Target OG')
        hSpace        =wx.StaticText(self,-1,'')
        
        descLabel.SetFont(wx.Font(pointSize=11,
                                  family=wx.FONTFAMILY_DEFAULT,
                                  weight=wx.FONTWEIGHT_BOLD,
                                  style=wx.FONTSTYLE_NORMAL))
                                          
        #Organize Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.AddSpacer((-1,25))
        
        #Add all Rows
        self.addRow([selectLabel, self.recipeSelection], vBox, 1)
        self.addRow([nameLabel, self.name], vBox, 1)
        self.addRow([batchSizeLabel, self.batchSize, hSpace, 
                     targetOGLabel, self.targetOG], vBox, 2)
        self.addRow([descLabel], vBox)
        self.addRow([self.description], vBox, 0, True)
        self.addRow([self.save], vBox)
        vBox.AddSpacer((-1,25))
        self.SetSizer(vBox)
        
        # Bindings
        self.Bind(wx.EVT_COMBOBOX, self.ChangeRecipe, self.recipeSelection) 
        self.Bind(wx.EVT_TEXT, self.UpdateRecipeData, self.batchSize)
        self.Bind(wx.EVT_TEXT, self.UpdateRecipeData, self.targetOG)
        self.Bind(wx.EVT_TEXT, self.UpdateRecipeData, self.name)
        self.Bind(wx.EVT_TEXT, self.UpdateRecipeData, self.description)
        self.Bind(wx.EVT_BUTTON, self.SaveRecipe, self.save)
        
    #----------------------------------------------------------------------
    def UpdateRecipeData(self, event):
        """ Update recipe values """
        self.recipe.name = self.name.GetValue()
        self.recipe.description = self.description.GetValue()
        self.recipe.targetOG = GetFloat(self.targetOG.GetValue())
        self.recipe.batchSize = GetFloat(self.batchSize.GetValue())
        origRecipe = self.parent.data.recipes[self.parent._dispID]
        self.save.Enable(self.recipe != origRecipe)
        self.parent.parent.parent.CheckSave()
        
    #----------------------------------------------------------------------
    def ChangeRecipe(self, event):
        """
        Respond to a change in the currently selected recipe. First check if
        a save is needed. If so, let the user veto it here before passing the
        change to the parent.
        """
        doChange = True
        if self.recipe != self.parent.data.recipes[self.parent._dispID]:
            ans = pyBrew.dialogs.SaveMessage(self.recipe.name).ShowModal()
            if ans == wx.ID_YES:
                self.SaveRecipe()
            doChange = (ans == wx.ID_NO or ans == wx.ID_YES)
        if doChange:
            self.parent.ChangeActiveDataItem(event.GetSelection(), False)
            self.LoadData()
        else:
            self.recipeSelection.SetSelection(self.parent._dispID)
            
    #----------------------------------------------------------------------
    def SaveRecipe(self, event=None):
        self.save.Enable(False)
        self.parent.Save('recipe')
                
    #----------------------------------------------------------------------
    def addRow(self, entries, vBox, scaledID=-1, vExp=False):
        """ Add a new row to the panel sizer """
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.AddSpacer((20,-1))
        for id, entry in enumerate(entries):
            hBox.Add(entry, proportion=(1 if scaledID == id else 0), 
                    flag=wx.ALL|(wx.EXPAND if vExp else 
                          wx.ALIGN_CENTER_VERTICAL), border=5)
        hBox.AddSpacer((20,-1))
        vBox.Add(hBox, proportion=(1 if vExp else 0), flag=wx.EXPAND)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in Panels.Recipe.Main"
        self.recipe = self.parent._activeDataItem
        self.recipeID = self.parent._dispID
        try:
            self.recipeSelection.Clear()
            self.recipeSelection.AppendItems(self.data.getRecipeNames())
            self.recipeSelection.SetSelection(self.recipeID)
            self.name.ChangeValue(self.recipe.name)
            self.description.ChangeValue(self.recipe.description)
            self.batchSize.ChangeValue(NumString(self.recipe.batchSize))
            self.targetOG.ChangeValue(NumString(self.recipe.targetOG,'Gravity'))
            origRecipe = self.parent.data.recipes[self.parent._dispID]
            self.save.Enable(self.recipe != origRecipe)
            self.parent.parent.parent.CheckSave()
        except AttributeError:
            pass
        
        
###############################################################################
class Ingredients(wx.Panel):
    """
    This is the recipe ingredients panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        
        # Make items
        self.ingredients = pyBrew.panels.ListPane(self, 
                           [(0, 'Item Name', 250),
                            (1, 'Amount', 120)],
                           [pyBrew.dialogs.AddFermDialog,
                            pyBrew.dialogs.AddHopDialog,
                            pyBrew.dialogs.AddYeastDialog,
                            pyBrew.dialogs.AddOtherDialog],
                           (-1,-1), ['Grain','Hop','Yeast','Other'])

        #Arrange Layout
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.ingredients, 1, wx.EXPAND)
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(hBox, 1, wx.EXPAND|wx.ALL, 20)
        
        self.SetSizer(vBox)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in Panels.Recipe.Ingredients"
        self.recipe = self.parent._activeDataItem
        self.ingredients.dataLists = [self.recipe.fermentables,
                                      self.recipe.hops,
                                      self.recipe.yeasts,
                                      self.recipe.otherIngredients]
        self.ingredients.UpdateValues()
        
    #----------------------------------------------------------------------
    def UpdateCalcValues(self):
        pass
  
        
###############################################################################
class Instructions(wx.Panel):
    """
    This is the recipe instructions
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        self.project = None
        self.projID = -1
        
        self.instructions = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        instructionsLabel = wx.StaticText(self, -1, 'Instructions')
        instructionsLabel.SetFont(wx.Font(pointSize=11,
                                          family=wx.FONTFAMILY_DEFAULT,
                                          weight=wx.FONTWEIGHT_BOLD,
                                          style=wx.FONTSTYLE_NORMAL))
        
        #Arrange Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        
        #Instructions Label
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(instructionsLabel,0,
                       wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL,20)
        
        #Instructions Box
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.instructions,1,wx.BOTTOM|wx.EXPAND,25)
        
        #Add all hBoxes to vBox
        for index, hBox in enumerate(hBoxes):
            vBox.Add(hBox, index, wx.LEFT|wx.RIGHT|wx.EXPAND, 25)
        
        self.SetSizer(vBox)
        
        self.Bind(wx.EVT_TEXT, self.UpdateData, self.instructions)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in Panels.Recipe.Instructions"
        self.recipe = self.parent._activeDataItem
        self.instructions.ChangeValue(self.recipe.instructions)
                               
    #----------------------------------------------------------------------
    def UpdateData(self, event):
        self.recipe.instructions = self.instructions.GetValue()
        
        
