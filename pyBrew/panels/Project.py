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

from pyBrew.pyBrewMethods import *
import pyBrew.Databases
import pyBrew.dialogs

###############################################################################
class Main(wx.Panel):
    """
    This is the main project panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """ Create the panel. This is called only when the program opens """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        self.project = None
        self.projID = -1
        
        #Grab the root data object
        self.data = parent.parent.parent.data
        
        #Define header font
        headerFont = wx.Font(pointSize=12,
                             family=wx.FONTFAMILY_DEFAULT,
                             weight=wx.FONTWEIGHT_BOLD,
                             style=wx.FONTSTYLE_NORMAL)

        #Create all editable/controllable items
        styleNames = pyBrew.Databases.StyleDb.GetNameList()
        self.projSelection   = wx.ComboBox(self, -1, style=wx.CB_READONLY)
        self.name            = wx.TextCtrl(self, -1)
        self.projectStyle    = wx.ComboBox(self, -1, choices=styleNames,
                                           style=wx.CB_READONLY)
        self.recipe          = wx.ComboBox(self, -1, style=wx.CB_READONLY)
        self.toggleRecipe    = wx.Button(self, -1, 'Show Recipe')
        self.brewDate        = wx.TextCtrl(self, -1, size=(100, -1))
        self.batchSize       = wx.TextCtrl(self, -1, size=(100,-1))
        self.boilSize        = wx.TextCtrl(self, -1, size=(100,-1))
        self.boilTime        = wx.TextCtrl(self, -1, size=(100,-1))
        self.daysInPrimary   = wx.TextCtrl(self, -1, size=(100,-1))
        self.daysInSecondary = wx.TextCtrl(self, -1, size=(100,-1))
        self.tankLoss        = wx.TextCtrl(self, -1, size=(100,-1))
        self.save            = wx.Button(self, wx.ID_SAVE, 'Save Changes')
        self.save.Enable(False)
        self.toggleRecipe.Enable(False) #Enable when feature works
        
        #Create all labels
        selectLabel = wx.StaticText(self, -1, 'Select Project')
        selectLabel.SetFont(headerFont)
        maxSize = selectLabel.GetSize()
        labSize = (maxSize[0],-1)
        
        nameLabel = wx.StaticText(self, -1, 'Project Name', size=labSize)
        styleLabel = wx.StaticText(self, -1, 'Project Style', size=labSize)
        recipeLabel = wx.StaticText(self, -1, 'Project Recipe', size=labSize)
        brewDateLabel = wx.StaticText(self, -1, 'Brew Date', size=labSize)
        batchSizeLabel = wx.StaticText(self, -1, 'Batch Size', size=labSize)
        boilSizeLabel = wx.StaticText(self, -1, 'Boil Size', size=labSize)
        boilTimeLabel = wx.StaticText(self, -1, 'Boil Time', size=labSize)
        dIPLabel = wx.StaticText(self, -1, 'Days in Primary', size=labSize)
        dISLabel = wx.StaticText(self, -1, 'Days in Secondary', size=labSize)
        tankLossLabel = wx.StaticText(self, -1, 'Tank Loss', size=labSize)
        minuteLabel = wx.StaticText(self, -1, 'minutes')
        gallonLabels = [wx.StaticText(self, -1, 'gallons'),
                        wx.StaticText(self, -1, 'gallons'),
                        wx.StaticText(self, -1, 'gallons')]
        
        #Organize Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.AddSpacer((-1,20))
        
        #Add all Rows
        self.addRow([selectLabel, self.projSelection], vBox, 1)
        self.addRow([nameLabel, self.name], vBox, 1)
        self.addRow([styleLabel, self.projectStyle], vBox, 1)
        self.addRow([recipeLabel, self.recipe, self.toggleRecipe], vBox, 1)
        self.addRow([brewDateLabel, self.brewDate], vBox)
        self.addRow([batchSizeLabel, self.batchSize, gallonLabels[0]], vBox)
        self.addRow([boilSizeLabel, self.boilSize, gallonLabels[1]], vBox)
        self.addRow([boilTimeLabel, self.boilTime, minuteLabel], vBox)
        self.addRow([dIPLabel, self.daysInPrimary], vBox)
        self.addRow([dISLabel, self.daysInSecondary], vBox)
        self.addRow([tankLossLabel, self.tankLoss, gallonLabels[2]], vBox)
        self.addRow([self.save], vBox)
        
        #ComboBox bindings
        self.Bind(wx.EVT_COMBOBOX, self.ChangeProject, self.projSelection)
        self.Bind(wx.EVT_COMBOBOX, self.ChangeStyle, self.projectStyle)
        
        #Text field bindings
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.batchSize)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.boilSize)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.tankLoss)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.name)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.brewDate)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.boilTime)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.daysInPrimary)
        self.Bind(wx.EVT_TEXT, self.UpdateProjectData, self.daysInSecondary)
        
        #Launch the calendar popup when the date box is clicked
        #self.brewDate.Bind(wx.EVT_LEFT_DOWN, self.clickedDate)
        
        #Set the save button
        self.Bind(wx.EVT_BUTTON, self.SaveProject, self.save)
        
        #Set the panel sizer
        self.SetSizer(vBox)
        
    #----------------------------------------------------------------------
    def clickedDate(self, event):
        pyBrew.dialogs.Calendar(self,-1,"Select Date",self.brewDate).ShowModal()
    
    #----------------------------------------------------------------------
    def ChangeStyle(self, event):
        self.project.style=pyBrew.BrewObjects.Style(self.projectStyle.GetValue())
        self.projectStyle.SetSelection(
                pyBrew.Databases.StyleDb.GetID(self.projectStyle.GetValue()))
        self.projectStyle.SetValue(self.project.style.name)
        origProject = self.parent.data.projects[self.parent._dispID]
        self.save.Enable(self.project != origProject)
        self.parent.parent.parent.CheckSave()
       
    #----------------------------------------------------------------------
    def UpdateProjectData(self, event):
        """ Update project values """
        self.project.name = self.name.GetValue()
        self.project.brewDate = self.brewDate.GetValue()
        self.project.boilTime = GetFloat(self.boilTime.GetValue())
        self.project.tankLoss = GetFloat(self.tankLoss.GetValue())
        self.project.boilSize = GetFloat(self.boilSize.GetValue())
        self.project.batchSize = GetFloat(self.batchSize.GetValue())
        self.project.daysInPrimary = GetFloat(self.daysInPrimary.GetValue())
        self.project.daysInSecondary=GetFloat(self.daysInSecondary.GetValue())
        self.project.boilTime = GetFloat(self.boilTime.GetValue())
        origProject = self.parent.data.projects[self.parent._dispID]
        self.save.Enable(self.project != origProject)
        self.parent.parent.parent.CheckSave()

    #----------------------------------------------------------------------
    def ChangeProject(self, event):
        doChange = True
        if self.project != self.parent.data.projects[self.parent._dispID]:
            ans = pyBrew.dialogs.SaveMessage(self.project.name).ShowModal()
            if ans == wx.ID_YES:
                self.SaveProject()
            doChange = (ans == wx.ID_NO or ans == wx.ID_YES)
        if doChange:
            self.parent.ChangeActiveDataItem(event.GetSelection(), False)
            self.LoadData()
        else:
            self.projSelection.SetSelection(self.parent._dispID)

    #----------------------------------------------------------------------
    def SaveProject(self, event=None):
        self.save.Enable(False)
        self.parent.Save('project')
    
    #----------------------------------------------------------------------
    def addRow(self, entries, vBox, scaledID=-1):
        """ Add a new row to the panel sizer """
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.AddSpacer((15,-1))
        for id, entry in enumerate(entries):
            hBox.Add(entry, proportion=(1 if scaledID == id else 0), 
                     flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        hBox.AddSpacer((15,-1))
        vBox.Add(hBox, proportion=0, flag=wx.EXPAND)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        """ Load data to display from the parent's activeDataItem """
        
        self.project = self.parent._activeDataItem
        self.projID = self.parent._dispID
        
        try:
            #Set ComboBox dropdown options
            #TODO: The project names need to use the current name, not the old name
            self.projSelection.Clear()
            self.projSelection.AppendItems(self.data.getProjectNames())
            self.projSelection.SetSelection(self.projID)
            
            self.recipe.Clear()
            self.recipe.AppendItems(self.data.getRecipeNames())
            
            #Load all other values
            self.name.ChangeValue(self.project.name)
            self.brewDate.ChangeValue(self.project.brewDate)
            self.batchSize.ChangeValue(NumString(self.project.batchSize))
            self.boilSize.ChangeValue(NumString(self.project.boilSize))
            self.boilTime.ChangeValue(NumString(self.project.boilTime,'Int'))
            self.daysInPrimary.ChangeValue(
                NumString(self.project.daysInPrimary,'Int'))
            self.daysInSecondary.ChangeValue(
                NumString(self.project.daysInSecondary,'Int'))
            self.tankLoss.ChangeValue(NumString(self.project.tankLoss))
            self.projectStyle.SetSelection(
                pyBrew.Databases.StyleDb.GetID(self.project.style.name))
            self.projectStyle.SetValue(self.project.style.name)
            origProject = self.parent.data.projects[self.parent._dispID]
            self.save.Enable(self.project != origProject)
            self.parent.parent.parent.CheckSave()
        except AttributeError:
            pass
     
     
###############################################################################
class Fermentables(wx.Panel):
    """
    This is the project fermentables panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        self.project = None
        
        #Define fonts and Colors
        calcColor = (200,200,200)
        styleColor = (255,128,0)
        
        #Items
        self.fermList = pyBrew.panels.ListPane(self, 
                           [(0, 'Item Name', 200),
                            (1, 'Amount', 100),
                            (2, 'Potential', -1),
                            (3, 'Gravity', 60),
                            (4, 'Percent', 60),
                            (5, 'Color Units', -1)],
                           [pyBrew.dialogs.AddFermDialog],
                           (-1,250), ['Grain'])
                                               
        roStyle = wx.TE_READONLY|wx.TE_CENTER
        self.styleOG    =wx.TextCtrl(self,-1,size=(100,-1),style=roStyle)
        self.totalColor =wx.TextCtrl(self,-1,size=(85,-1), style=roStyle)
        self.calcOG     =wx.TextCtrl(self,-1,size=(100,-1),style=roStyle)
        self.styleSRM   =wx.TextCtrl(self,-1,size=(85,-1), style=roStyle)
        self.boilOG     =wx.TextCtrl(self,-1,size=(100,-1),style=roStyle)
        self.calcSRM    =wx.TextCtrl(self,-1,size=(85,-1), style=roStyle)
        self.actualOG   =wx.TextCtrl(self,-1,size=(100,-1),style=wx.TE_CENTER) 
        self.actualColor=wx.TextCtrl(self,-1,size=(85,-1), style=wx.TE_CENTER)

        self.styleOG.SetBackgroundColour(styleColor)
        self.totalColor.SetBackgroundColour(calcColor)
        self.calcOG.SetBackgroundColour(calcColor)
        self.styleSRM.SetBackgroundColour(styleColor)
        self.boilOG.SetBackgroundColour(calcColor)
        self.calcSRM.SetBackgroundColour(calcColor)
        
        #Labels
        styleOGLabel     = wx.StaticText(self, -1, 'Style O.G. Range', 
                                         style=wx.ALIGN_RIGHT)
        totalColorLabel  = wx.StaticText(self, -1, 'Total Color Units',
                                         style=wx.ALIGN_RIGHT)
        calcOGLabel      = wx.StaticText(self, -1, 'Predicted O.G.',
                                         style=wx.ALIGN_RIGHT)
        styleSRMLabel    = wx.StaticText(self, -1, 'Style SRM',
                                         style=wx.ALIGN_RIGHT)
        boilOGLabel      = wx.StaticText(self, -1, 'Boil O.G.',
                                         style=wx.ALIGN_RIGHT)
        calcSRMLabel     = wx.StaticText(self, -1, 'Predicted SRM',
                                         style=wx.ALIGN_RIGHT)
        actualOGLabel    = wx.StaticText(self, -1, 'Actual O.G.',
                                         style=wx.ALIGN_RIGHT)
        actualColorLabel = wx.StaticText(self, -1, 'Actual Color',
                                         style=wx.ALIGN_RIGHT)
        
        #Organize Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        vBoxes = []
        
        #Main List
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.fermList, 1, wx.EXPAND|wx.ALL, 10)
        
        #Calculations row
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        vBoxes.append(wx.BoxSizer(wx.VERTICAL))
        vBoxes[-1].AddSpacer((-1,10))
        self.addRow([calcOGLabel, self.calcOG], vBoxes[-1])
        self.addRow([styleOGLabel, self.styleOG], vBoxes[-1])
        self.addRow([boilOGLabel, self.boilOG], vBoxes[-1])
        self.addRow([actualOGLabel, self.actualOG], vBoxes[-1])
        vBoxes.append(wx.BoxSizer(wx.VERTICAL))
        vBoxes[-1].AddSpacer((-1,10))
        self.addRow([totalColorLabel, self.totalColor], vBoxes[-1])
        self.addRow([styleSRMLabel, self.styleSRM], vBoxes[-1])
        self.addRow([calcSRMLabel, self.calcSRM], vBoxes[-1])
        self.addRow([actualColorLabel, self.actualColor], vBoxes[-1])

        hBoxes[-1].AddSpacer((-1,-1), proportion=1)
        hBoxes[-1].Add(vBoxes[-2], proportion=0)
        hBoxes[-1].AddSpacer((30,-1))
        hBoxes[-1].Add(vBoxes[-1], proportion=0)
        hBoxes[-1].AddSpacer((15,-1))
        
        #Add all hBoxes to vBox
        for hBox in hBoxes:
            vBox.Add(hBox, 0, wx.EXPAND)
        
        self.SetSizer(vBox)
        
        #Text box bindings
        self.Bind(wx.EVT_TEXT, self.updateActualOG,  self.actualOG)
        self.Bind(wx.EVT_TEXT, self.updateActualColor,  self.actualColor)
        
    #----------------------------------------------------------------------
    def updateActualOG(self, event):
        """ Update project actual OG and recalculate values """
        newActualOG = GetFloat(self.actualOG.GetValue())
        self.project.actualOG = newActualOG
        self.project.CalcValues()
        self.UpdateCalcValues()
        self.fermList.UpdateValues()
    
    #----------------------------------------------------------------------
    def updateActualColor(self, event):
        """ Update project actual color """
        self.project.actualColor = GetFloat(self.actualColor.GetValue())
    
    #----------------------------------------------------------------------
    def addRow(self, entries, vBox):
        """ Add a new row to the panel sizer """
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        for id, entry in enumerate(entries):
            hBox.Add(entry, proportion=0, 
                     flag=wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP,
                     border=5)
        vBox.Add(hBox, proportion=0, flag=wx.ALIGN_RIGHT)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in panels.Project.Grains"
        self.project = self.parent._activeDataItem
        self.actualOG.ChangeValue(NumString(self.project.actualOG,'Gravity'))
        self.actualColor.ChangeValue(NumString(self.project.actualColor,'Int'))
        self.styleOG.ChangeValue(self.project.style.OG.Format('Gravity'))
        self.styleSRM.ChangeValue(self.project.style.SRM.Format('Int'))
        self.fermList.dataLists = [self.project.fermentables]
        self.UpdateCalcValues()
        self.fermList.UpdateValues()

    #----------------------------------------------------------------------
    def UpdateCalcValues(self):
        self.project.CalcValues()
        self.calcOG.ChangeValue(NumString(self.project.calcOG,'Gravity'))
        self.totalColor.ChangeValue(NumString(self.project.totalColor,'Int'))
        self.calcSRM.ChangeValue(NumString(self.project.calcSRM,'Int'))
        self.boilOG.ChangeValue(NumString(self.project.boilOG,'Gravity'))


###############################################################################
class Hops(wx.Panel):
    """
    This is the project hops panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        self.project = None
        
        #Define fonts and Colors
        calcColor = (200,200,200)
        styleColor = (255,128,0)
        
        #Labels
        hopFormulaLabel = wx.StaticText(self, -1, 'Hop Formula')
        BUGULabel = wx.StaticText(self, -1, 'BU/GU Ratio')
        totalIBULabel = wx.StaticText(self, -1, 'Total IBU')
        styleIBULabel = wx.StaticText(self, -1, 'Style IBU')
        
        #Items
        self.hopList = pyBrew.panels.ListPane(self, 
                           [(0, 'Item Name', 200),
                            (1, 'oz.', 50),
                            (2, 'Boil Time', -1),
                            (3, 'AAU', 50),
                            (4, 'Form', -1),
                            (5, 'Use (%)', -1),
                            (6, 'IBU', 50)],
                           [pyBrew.dialogs.AddHopDialog],
                           (-1,250), ['Hop'])

        self.hopFormula = wx.ComboBox(self, -1, 
                                choices=pyBrew.Databases.HopDb.FormulaNames,
                                size=(130,-1), style=wx.CB_READONLY)
                                      
        self.BUGU     = wx.TextCtrl(self, -1, size=(100,-1),
                                    style=wx.TE_READONLY|wx.TE_CENTER)
        self.totalIBU = wx.TextCtrl(self, -1, size=(100,-1),
                                    style=wx.TE_READONLY|wx.TE_CENTER) 
        self.styleIBU = wx.TextCtrl(self, -1, size=(100,-1),
                                    style=wx.TE_READONLY|wx.TE_CENTER)

        self.BUGU.SetBackgroundColour(calcColor)
        self.totalIBU.SetBackgroundColour(calcColor)
        self.styleIBU.SetBackgroundColour(styleColor)
        
        #Organize Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        vBoxes = []
        
        #Hop List
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.hopList, 1, wx.EXPAND|wx.ALL, 10)
        
        #Calculation row
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        vBoxes.append(wx.BoxSizer(wx.VERTICAL))
        vBoxes[-1].AddSpacer((-1,10))
        self.addRow([BUGULabel, self.BUGU], vBoxes[-1])
        self.addRow([totalIBULabel, self.totalIBU], vBoxes[-1])
        self.addRow([styleIBULabel, self.styleIBU], vBoxes[-1])
        hBoxes[-1].Add(hopFormulaLabel,0,wx.LEFT|wx.ALIGN_CENTER_VERTICAL,20)
        hBoxes[-1].Add(self.hopFormula,0,wx.LEFT|wx.ALIGN_CENTER_VERTICAL,5)
        hBoxes[-1].AddSpacer((-1,-1), proportion=1)
        hBoxes[-1].Add(vBoxes[-1], proportion=0)
        hBoxes[-1].AddSpacer((15,-1))
        
        #Add all hBoxes to vBox
        for hBox in hBoxes:
            vBox.Add(hBox, proportion=0, flag=wx.EXPAND)
            
        self.SetSizer(vBox)
        
        self.Bind(wx.EVT_COMBOBOX, self.UpdateHopFormula, self.hopFormula)
        
    #----------------------------------------------------------------------
    def UpdateHopFormula(self, event):
        """ Update project hop formula and recalculate values """
        self.project.hopFormulaName = self.hopFormula.GetValue()
        self.project.CalcValues()
        self.UpdateCalcValues()
        self.hopList.UpdateValues()
        
    #----------------------------------------------------------------------
    def addRow(self, entries, vBox):
        """ Add a new row to the panel sizer """
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        for id, entry in enumerate(entries):
            hBox.Add(entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        vBox.Add(hBox, 0, wx.ALIGN_RIGHT)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in panels.Project.Hops"
        self.project = self.parent._activeDataItem
        self.hopFormula.SetSelection(
            pyBrew.Databases.HopDb.FormulaNames.index(
                self.project.hopFormulaName))
        self.styleIBU.ChangeValue(self.project.style.IBU.Format('Int'))
        self.hopList.dataLists = [self.project.hops]
        self.UpdateCalcValues()
        self.hopList.UpdateValues()

    #----------------------------------------------------------------------
    def UpdateCalcValues(self):
        self.project.CalcValues()
        self.BUGU.SetValue(NumString(self.project.BUGU))
        self.totalIBU.SetValue(NumString(self.project.totalIBU,'Int'))
                            
                            
###############################################################################
class Yeast(wx.Panel):
    """
    This is the project yeast panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        self.project = None
        
        #Define fonts and Colors
        calcColor = (200,200,200)
        styleColor = (255,128,0)
        
        #Items
        yeastNames = pyBrew.Databases.YeastDb.Names
        roStyle = wx.TE_READONLY|wx.TE_CENTER
        self.yeastType  = wx.ComboBox(self, -1, choices=yeastNames,
                                      size=(-1,-1), style=wx.CB_READONLY) 
        self.calcAtten  = wx.TextCtrl(self,-1,size=(90,-1), style=roStyle) 
        self.actualAtten= wx.TextCtrl(self,-1,size=(90,-1), style=roStyle) 
        self.styleAtten = wx.TextCtrl(self,-1,size=(90,-1), style=roStyle) 
        self.calcABV    = wx.TextCtrl(self,-1,size=(70,-1), style=roStyle) 
        self.actualABV  = wx.TextCtrl(self,-1,size=(70,-1), style=roStyle) 
        self.styleABV   = wx.TextCtrl(self,-1,size=(70,-1), style=roStyle) 
        self.calcABW    = wx.TextCtrl(self,-1,size=(70,-1), style=roStyle) 
        self.actualABW  = wx.TextCtrl(self,-1,size=(70,-1), style=roStyle) 
        self.styleABW   = wx.TextCtrl(self,-1,size=(70,-1), style=roStyle) 
        self.calcCal    = wx.TextCtrl(self,-1,size=(90,-1), style=roStyle) 
        self.actualCal  = wx.TextCtrl(self,-1,size=(90,-1), style=roStyle) 
        self.styleCal   = wx.TextCtrl(self,-1,size=(90,-1), style=roStyle) 
        self.calcFG     = wx.TextCtrl(self,-1,size=(100,-1),style=roStyle) 
        self.actualFG   = wx.TextCtrl(self,-1,size=(100,-1),style=wx.TE_CENTER) 
        self.styleFG    = wx.TextCtrl(self,-1,size=(100,-1),style=roStyle) 
        self.yeastDesc  = wx.StaticText(self,-1,'',(550,-1))
        self.yeastDesc.Wrap(550)
        
        self.styleAtten.SetBackgroundColour(styleColor)
        self.styleABV.SetBackgroundColour(styleColor)
        self.styleABW.SetBackgroundColour(styleColor)
        self.styleCal.SetBackgroundColour(styleColor)
        self.styleFG.SetBackgroundColour(styleColor)
        self.calcAtten.SetBackgroundColour(calcColor)
        self.actualAtten.SetBackgroundColour(calcColor)
        self.calcABV.SetBackgroundColour(calcColor)
        self.actualABV.SetBackgroundColour(calcColor)
        self.calcABW.SetBackgroundColour(calcColor)
        self.actualABW.SetBackgroundColour(calcColor)
        self.calcCal.SetBackgroundColour(calcColor)
        self.actualCal.SetBackgroundColour(calcColor)
        self.calcFG.SetBackgroundColour(calcColor)
        
        yeastDescLabel = wx.StaticBox(self, -1, 'Description', size=(570,300))
        boxsizer = wx.StaticBoxSizer(yeastDescLabel, wx.VERTICAL)
        boxsizer.Add(self.yeastDesc, 1, wx.ALL|wx.EXPAND, 5)
        predValLabel = wx.StaticText(self,-1,'Predicted Values')
        yeastTypeLabel = wx.StaticText(self,-1,'Yeast Type')
        wideLabSize = predValLabel.GetSize()
        ytLabSize = yeastTypeLabel.GetSize()
        buffer = wideLabSize[0] - ytLabSize[0]
        
        yeastDescLabel.SetFont(wx.Font(pointSize=11,
                               family=wx.FONTFAMILY_DEFAULT,
                               weight=wx.FONTWEIGHT_BOLD,
                               style=wx.FONTSTYLE_NORMAL))
                                  
        #Organize Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        
        #Yeast Type selector
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((buffer-2,-1))
        hBoxes[-1].Add(yeastTypeLabel,
                       flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM,
                       border=10)
        hBoxes[-1].AddSpacer((5,-1))
        hBoxes[-1].Add(self.yeastType, 1,
                       flag=wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, border=10)
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((-1,20))
        
        #Calculations grid
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((10,-1))
        gs = wx.FlexGridSizer(4, 6, 5, 5)
        gs.AddMany([(wx.StaticText(self,-1,''), 0),
                    (wx.StaticText(self,-1,'Attenuation'),0,wx.ALIGN_CENTER),
                    (wx.StaticText(self,-1,'ABV'),0,wx.ALIGN_CENTER),
                    (wx.StaticText(self,-1,'ABW'),0,wx.ALIGN_CENTER),
                    (wx.StaticText(self,-1,'Cal./16 oz.'),0,wx.ALIGN_CENTER),
                    (wx.StaticText(self,-1,'Final Gravity'),0,wx.ALIGN_CENTER),
                    (predValLabel,0,wx.ALIGN_RIGHT),
                    (self.calcAtten, 0, wx.EXPAND),
                    (self.calcABV, 0, wx.EXPAND),
                    (self.calcABW, 0, wx.EXPAND),
                    (self.calcCal, 0, wx.EXPAND),
                    (self.calcFG, 0, wx.EXPAND),
                    (wx.StaticText(self,-1,'Actual Values'),0,wx.ALIGN_RIGHT),
                    (self.actualAtten, 0, wx.EXPAND),
                    (self.actualABV, 0, wx.EXPAND),
                    (self.actualABW, 0, wx.EXPAND),
                    (self.actualCal, 0, wx.EXPAND),
                    (self.actualFG, 0, wx.EXPAND),
                    (wx.StaticText(self,-1,'Style Values'), 0, wx.ALIGN_RIGHT),
                    (self.styleAtten, 0, wx.EXPAND),
                    (self.styleABV, 0, wx.EXPAND),
                    (self.styleABW, 0, wx.EXPAND),
                    (self.styleCal, 0, wx.EXPAND),
                    (self.styleFG, 0, wx.EXPAND)])
        
        gs.AddGrowableCol(1,5)
        gs.AddGrowableCol(2,3)
        gs.AddGrowableCol(3,3)
        gs.AddGrowableCol(4,4)
        gs.AddGrowableCol(5,5)
        hBoxes[-1].Add(gs, 1, wx.ALIGN_RIGHT)
        hBoxes[-1].AddSpacer((10,-1))
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((-1,30))
        
        #Yeast description
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(boxsizer, 0, wx.ALL, 20)

        #Add all hBoxes to vBox
        for hBox in hBoxes:
            vBox.Add(hBox, proportion=0, flag=wx.EXPAND)
            
        self.SetSizer(vBox)
        
        self.Bind(wx.EVT_TEXT, self.updateActualFG,  self.actualFG)
        self.Bind(wx.EVT_COMBOBOX, self.updateYeastType, self.yeastType)
        
    #----------------------------------------------------------------------
    def updateActualFG(self, event):
        """ Update project actual FG and recalculate values """
        newActualFG = GetFloat(self.actualFG.GetValue())
        self.project.actualFG = newActualFG
        self.project.CalcValues()
        self.UpdateCalcValues()
        
    #----------------------------------------------------------------------
    def updateYeastType(self, event):
        """ Update project yeast type and recalculate values """
        self.project.yeast = pyBrew.BrewObjects.Yeast(self.yeastType.GetValue())
        desc = pyBrew.Databases.YeastDb.Description(self.yeastType.GetValue())
        self.yeastDesc.SetLabel(desc)
        self.yeastDesc.Wrap(550)
        self.project.CalcValues()
        self.UpdateCalcValues()
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in panels.Project.Yeast"
        self.project = self.parent._activeDataItem
        self.yeastType.SetSelection(
                pyBrew.Databases.YeastDb.GetID(self.project.yeast.name)) 
        desc = pyBrew.Databases.YeastDb.Description(self.project.yeast.name)
        self.yeastDesc.SetLabel(desc)
        self.yeastDesc.Wrap(450)
        self.actualFG.ChangeValue(NumString(self.project.actualFG,'Gravity'))
        self.styleFG.ChangeValue(self.project.style.FG.Format('Gravity'))
        self.styleAtten.ChangeValue(
                self.project.style.attenuation.Format('Int'))
        self.styleABV.ChangeValue(self.project.style.ABV.Format('Dec'))
        self.styleABW.ChangeValue(self.project.style.ABW.Format('Dec'))
        self.styleCal.ChangeValue(self.project.style.calories.Format('Dec'))
        self.UpdateCalcValues()
         
    #----------------------------------------------------------------------
    def UpdateCalcValues(self):
        self.project.CalcValues()
        self.actualAtten.SetValue(NumString(self.project.actualAtten,'Atten'))
        self.actualABW.SetValue(NumString(self.project.actualABW))
        self.actualABV.SetValue(NumString(self.project.actualABV))
        self.actualCal.SetValue(NumString(self.project.actualCal))
        self.calcAtten.SetValue(self.project.calcAtten.Format('Int'))
        self.calcFG.SetValue(self.project.calcFG.Format('Gravity'))
        self.calcABW.SetValue(self.project.calcABW.Format())
        self.calcABV.SetValue(self.project.calcABV.Format())
        self.calcCal.SetValue(self.project.calcCal.Format())
        
        
###############################################################################
class Other(wx.Panel):
    """
    This is the project other panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.parent = parent
        
        #Items
        self.otherList = pyBrew.panels.ListPane(self, 
                           [(0, 'Item Name', 250),
                            (1, 'Amount', 120)],
                           [pyBrew.dialogs.AddOtherDialog],
                           (-1,-1), ['Other'])
                           
        self.notes = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        notesLabel = wx.StaticText(self, -1, "Notes")
        notesLabel.SetFont(wx.Font(pointSize=11,
                                  family=wx.FONTFAMILY_DEFAULT,
                                  weight=wx.FONTWEIGHT_BOLD,
                                  style=wx.FONTSTYLE_NORMAL))
        #Organize layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        prop = []
        
        #Other Ingredients List
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.otherList, 1, wx.EXPAND|wx.ALL, 10)
        prop.append(1)
        
        #Notes
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].AddSpacer((15,-1))
        hBoxes[-1].Add(notesLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        prop.append(0)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.notes, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 20)
        prop.append(1)
        
        #Add all hBoxes to vBox
        for id, hBox in enumerate(hBoxes):
            vBox.Add(hBox, proportion=prop[id], flag=wx.EXPAND)
            
        self.SetSizer(vBox)
        self.Bind(wx.EVT_TEXT, self.UpdateData, self.notes)
        
    #----------------------------------------------------------------------
    def LoadData(self):
        #print "Load data in panels.Project.Other"
        self.project = self.parent._activeDataItem
        self.notes.ChangeValue(self.project.notes)
        self.otherList.dataLists = [self.project.otherIngredients]
        self.UpdateCalcValues()
        self.otherList.UpdateValues()
        
    #----------------------------------------------------------------------
    def UpdateData(self, event):
        self.project.notes = self.notes.GetValue()
        
    #----------------------------------------------------------------------
    def UpdateCalcValues(self):
        pass
  
