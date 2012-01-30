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

import copy
import wx
import pickle
import wx.lib.agw.labelbook as LB
import wx.lib.agw.flatnotebook as fnb

import panels
import BrewData
import dialogs

###############################################################################
class MainFrame(wx.Frame):
    """
    The main frame that contains the data object and top-level notebook
    """
    #----------------------------------------------------------------------
    def __init__(self):        
        wx.Frame.__init__(self, None, -1, "Homebrew Program", size=(820,650))
        
        #Get a data object, contained by this Frame
        self.data = BrewData.RootData().Load()
        
        #Create Menu bar and menus
        self.topMenu = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.projectMenu = wx.Menu()
        self.recipeMenu = wx.Menu()
        self.aboutMenu = wx.Menu()
        
        #File Menu
        self.mSave = self.fileMenu.Append(-1, '&Save All',
                                          'Save changes to project')

        self.fileMenu.AppendSeparator()
        self.mQuit = self.fileMenu.Append(-1, '&Exit', 'Quit program')
        
        #Project Menu
        self.mNewP = self.projectMenu.Append(-1,'&New Project','New Project')
        self.mDeleteP = self.projectMenu.Append(-1,'&Delete Project',
                                                'Delete Project')
        self.mExportP = self.projectMenu.Append(-1, '&Export Project',
                                          'Export project to text file')
        self.mImportP = self.projectMenu.Append(-1, '&Import Project',
                                          'Import project from text file')
                                          
        #Recipe Menu
        self.mNewR = self.recipeMenu.Append(-1,'&New Recipe','New Recipe')
        self.mDeleteR = self.recipeMenu.Append(-1,'&Delete Recipe',
                                               'Delete Recipe')
        self.mExportR = self.recipeMenu.Append(-1, '&Export Recipe',
                                          'Export recipe to text file')
        self.mImportR = self.recipeMenu.Append(-1, '&Import Recipe',
                                          'Import recipe from text file')        
        #About menu
        self.mAbout = self.aboutMenu.Append(-1, '&About', 'About')
        
        #Add Menus to Menu Bar and create a status bar
        self.topMenu.Append(self.fileMenu, '&File')
        self.topMenu.Append(self.projectMenu, '&Projects')
        self.topMenu.Append(self.recipeMenu, '&Recipes')
        self.topMenu.Append(self.aboutMenu, '&Help')
        self.SetMenuBar(self.topMenu)
                                          
        self.Notebook = MyNotebook(self)
        self.Notebook.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.Show()
        
        self.Bind(wx.EVT_CLOSE, self.ShutDown)
        self.Bind(wx.EVT_MENU, self.DoSaves, self.mSave)
        self.Bind(wx.EVT_MENU, self.ShutDown, self.mQuit)
        self.Bind(wx.EVT_MENU, self.ShowAbout, self.mAbout)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='New': self.ModifyItems(evt,act,'Project'),
            self.mNewP)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='Delete': self.ModifyItems(evt,act,'Project'),
            self.mDeleteP)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='Export': self.ModifyItems(evt,act,'Project'),
            self.mExportP)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='Import': self.ModifyItems(evt,act,'Project'),
            self.mImportP)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='New': self.ModifyItems(evt,act,'Recipe'),
            self.mNewR)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='Delete': self.ModifyItems(evt,act,'Recipe'),
            self.mDeleteR)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='Export': self.ModifyItems(evt,act,'Recipe'),
            self.mExportR)
        self.Bind(wx.EVT_MENU,
            lambda evt, act='Import': self.ModifyItems(evt,act,'Recipe'),
            self.mImportR)
        self.mSave.Enable(False)
       
    #----------------------------------------------------------------------
    def ShowAbout(self, event):
        dialogs.About(self).ShowModal()
        
    #----------------------------------------------------------------------
    def DoImport(self, type='Project'):
        dlg = dialogs.GetFilePath(self, type, 'Import')
        ans = dlg.ShowModal()
        if ans == wx.ID_OK:
            if type == 'Project':
                self.data.projects.append(BrewData.Project())
                imported = self.data.projects[-1].Import(dlg.GetPath())
                if not imported:
                    del self.data.projects[-1]
                    ed = dialogs.ImportError(dlg.GetFilename(),type).ShowModal()
            else:
                self.data.recipes.append(BrewData.Recipe())
                imported = self.data.recipes[-1].Import(dlg.GetPath())
                if not imported:
                    del self.data.recipes[-1]
                    ed = dialogs.ImportError(dlg.GetFilename(),type).ShowModal()
        dlg.Destroy()
        
    #----------------------------------------------------------------------
    def DoExport(self, id, type='Project'):
        dlg = dialogs.GetFilePath(self, type, 'Export')
        ans = exportDlg.ShowModal()
        if ans == wx.ID_OK:
            if type == 'Project':
                self.data.projects[id].Export(dlg.GetPath())
            else:
                self.data.recipes[id].Export(dlg.GetPath())
        dlg.Destroy()
        
        
    #----------------------------------------------------------------------
    def ModifyItems(self, event, action='New', type='Project'):
        if action == 'Import':
            self.DoImport(type)
        else:
            dlg = dialogs.ModifyTopItems(self, action, type)
            ans = dlg.ShowModal()
            if ans == wx.ID_OK:
                if action == 'New':
                    if type == 'Project':
                        self.data.projects.append(
                            BrewData.Project(dlg.text.GetValue()))
                    else:
                        self.data.recipes.append(
                            BrewData.Recipe(dlg.text.GetValue()))
                            
                elif action == 'Delete':
                    id = dlg.text.GetSelection()
                    if id >= 0:
                        if type == 'Project':
                            self.DeleteProject(id)
                        else:
                            self.DeleteRecipe(id)
                                
                elif action == 'Export':
                    self.DoExport(dlg.text.GetSelection(), type)
                    
            dlg.Destroy()
        self.Notebook.browser.LoadActivePanel()
        
    #----------------------------------------------------------------------
    def DeleteProject(self, id):
        ans = dialogs.ConfirmDelete(self.data.projects[id].name).ShowModal()
        if ans == wx.ID_YES:
            del self.data.projects[id]
            self.Notebook.projectBook._activeDataItem = None
            self.Notebook.projectBook.ChangeActiveDataItem(0,False)
            self.Notebook.projectBook.LoadActivePanel()
    
    #----------------------------------------------------------------------
    def DeleteRecipe(self, id):
        ans = dialogs.ConfirmDelete(self.data.recipes[id].name).ShowModal()
        if ans == wx.ID_YES:
            del self.data.recipes[id]
            self.Notebook.recipeBook._activeDataItem = None
            self.Notebook.recipeBook.ChangeActiveDataItem(0,False)
            self.Notebook.recipeBook.LoadActivePanel()
    
    #----------------------------------------------------------------------
    def CheckSave(self):
        projID = self.Notebook.projectBook._dispID
        editedProject = self.Notebook.projectBook._activeDataItem
        recipeID = self.Notebook.recipeBook._dispID
        editedRecipe = self.Notebook.recipeBook._activeDataItem
        
        try:
            changedRecipe = editedRecipe != self.data.recipes[recipeID]
        except IndexError:
            changedRecipe = False
            
        try:
            changedProject = editedProject != self.data.projects[projID]
        except IndexError:
            changedProject = False
        
        self.mSave.Enable(changedRecipe or changedProject)
    
    #----------------------------------------------------------------------
    def DoSaves(self, event):
        self.Notebook.projectBook.Save('project')
        self.Notebook.recipeBook.Save('recipe')
        self.CheckSave()

    #----------------------------------------------------------------------
    def ShutDown(self, event):
        projID = self.Notebook.projectBook._dispID
        editedProject = self.Notebook.projectBook._activeDataItem
        recipeID = self.Notebook.recipeBook._dispID
        editedRecipe = self.Notebook.recipeBook._activeDataItem
        closeWindow = True
        
        try:
            if editedProject != self.data.projects[projID]:
                ans = dialogs.SaveMessage(editedProject.name).ShowModal()
                if ans == wx.ID_YES:
                    self.Notebook.projectBook.Save('project')
                closeWindow = (ans == wx.ID_NO or ans == wx.ID_YES)
        except IndexError:
            pass
        
        try:
            if closeWindow and editedRecipe != self.data.recipes[recipeID]:
                ans = dialogs.SaveMessage(editedRecipe.name).ShowModal()
                if ans == wx.ID_YES:
                    self.Notebook.recipeBook.Save('recipe')
                closeWindow = (ans == wx.ID_NO or ans == wx.ID_YES)
        except IndexError:
            pass
            
        #If we don't destroy the Notebook first, this causes a segfault when
        # closed from the Recipe notebook tab. It seems as it destroys the
        # tabs it then tries to load the next available tab, which causes
        # issues.
        if closeWindow:
            self.Notebook.Destroy()
            self.Destroy()


###############################################################################
class MyLabelBook(LB.LabelBook):
    """
    Labelbook class displays project and recipe windows with the graphical
    menu on the left side of the panel.
    """
    #----------------------------------------------------------------------
    def __init__(self, parent, type):
        LB.LabelBook.__init__(self, parent, agwStyle=LB.INB_FIT_LABELTEXT|
                              LB.INB_LEFT|LB.INB_DRAW_SHADOW|LB.INB_BORDER,
                              name=type)
        self.parent = parent
        self.data = self.parent.parent.data
        self.type = type
        self._activeDataItem = None
        self.ChangeActiveDataItem(0)
        self.Bind(LB.EVT_IMAGENOTEBOOK_PAGE_CHANGED, self.LoadActivePanel)
        
    #----------------------------------------------------------------------
    def SetPages(self, pages, width=160):          
        # Make an image list from png icons
        imList = wx.ImageList(50, 50)
                 
        # Add pages and associate with icons
        for imID, (page, label, imName) in enumerate(pages):
            self.AddPage(page, label, imageId=imID)
            imList.Add(wx.Bitmap('pyBrew/icons/' + imName))
        self.AssignImageList(imList)
        
        # Force a constant tab area width and set the color
        self._pages.SetTabAreaWidth(width)
        self._pages.SetSizeHints(width, -1)
        self._pages.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR,
                              wx.Color(255,255,255))
        
    #----------------------------------------------------------------------
    def LoadActivePanel(self, event=None):
        self.GetChildren()[self.GetSelection()+1].LoadData()
       
    #----------------------------------------------------------------------
    def Save(self, type):
        if type == 'project':
            self.data.projects[self._dispID] = self._activeDataItem
        elif type == 'recipe':
            self.data.recipes[self._dispID] = self._activeDataItem
        pickle.dump(self.data, open('mydata.brew', 'wb') ,-1)
        self.ChangeActiveDataItem(self._dispID)
        self.LoadActivePanel()
        self.parent.parent.CheckSave()
        
    #----------------------------------------------------------------------
    def ChangeActiveDataItem(self, newID, confirmChange=True):
        try:
            doChange = True
            if self._activeDataItem is not None:
                original = (self.data.projects[self._dispID] if 
                    self.type == 'project' else self.data.recipes[self._dispID])
            
                if original != self._activeDataItem and confirmChange:
                    ans=dialogs.SaveMessage(self._activeDataItem.name).ShowModal()
                    if ans == wx.ID_YES:
                        self.Save(self.type)
                    doChange = (ans != wx.ID_YES and ans != wx.ID_NO)
                
            if doChange:
                self._activeDataItem = copy.deepcopy(self.data.projects[newID] 
                    if self.type == 'project' else self.data.recipes[newID])
                self._dispID = newID
        except IndexError:
            self._dispID = -1
            self._activeDataItem = None


###############################################################################
class MyNotebook(fnb.FlatNotebook): #wx.Notebook):
    """
    My custom notebook class. This is where pages are organized and subpanels
    are called in.
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        fnb.FNB_HEIGHT_SPACER = 20
        fnb.FlatNotebook.__init__(self, parent, id=wx.ID_ANY,
                                  agwStyle=fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_FANCY_TABS|fnb.FNB_NODRAG) #, style=wx.BK_TOP)
        
        #Keep track of who the parent is
        self.parent = parent
        
        #Add Browser panel
        self.browser = panels.Browser(self)
        self.AddPage(self.browser, "Home")
        
        #Add Calendar panel
        self.calendar = panels.Calendar(self)
        self.AddPage(self.calendar, "Calendar")
        
        #Add panels with ListBook nav windows
        self.projectBook = MyLabelBook(self,'project')
        self.recipeBook  = MyLabelBook(self,'recipe')
        
        #Define which pages are in the ListBook panels
        projectPages = [(panels.Project.Main(self.projectBook), 
                            "Overview", "beer.png"),
                        (panels.Project.Fermentables(self.projectBook), 
                            "Grains", "grains.png"),
                        (panels.Project.Hops(self.projectBook), 
                            "Hops", "hops.png"),
                        (panels.Project.Yeast(self.projectBook), 
                            "Yeast", "yeast.png"),
                        (panels.Project.Other(self.projectBook), 
                            "Other", "beercap.png")]
                 
        recipePages = [(panels.Recipe.Main(self.recipeBook), 
                            "Overview", "beer.png"),
                       (panels.Recipe.Ingredients(self.recipeBook), 
                            "Ingredients", "grains.png"),
                       (panels.Recipe.Instructions(self.recipeBook), 
                            "Instructions", "instructions.png")]
        
        #Add ListBook items to tab panel
        self.AddPage(self.projectBook, "Projects")
        self.projectBook.SetPages(projectPages,160)
        
        self.AddPage(self.recipeBook, "Recipes")
        self.recipeBook.SetPages(recipePages,160)

        #Add Style panel
        self.styles = panels.Styles(self)
        self.AddPage(self.styles, "Styles")
        
        #Make the tabs extra wide
        #self.SetPadding(40)
        #print self.PageInfo
        self._nPadding = 30
        
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnPageClosing)
        
    #----------------------------------------------------------------------
    def OnPageClosing(self, event):
        event.Veto()
        
    #----------------------------------------------------------------------
    def OnPageChanging(self, event):
        """ 
        Allow a page change unless the item being changed to is an empty list,
        in which case, veto the page change.
        """
        name=event.EventObject.GetChildren()[event.GetSelection()+1].GetName()
        allow = True
        if name == 'project':
            allow = self.parent.data.projects
        elif name == 'recipe':
            allow = self.parent.data.recipes
        
        if allow:
            event.Skip()
        else:
            event.Veto()

    #----------------------------------------------------------------------
    def OnPageChanged(self, event):
        self.GetChildren()[event.GetSelection()+1].LoadActivePanel()
        event.Skip()
       
    #----------------------------------------------------------------------
    def SetToProjects(self, id):
        self.projectBook.ChangeActiveDataItem(id) #Load project 'id'
        self.projectBook.SetSelection(0)          #Set to overview tab
        self.SetSelection(2)                      #Switch to projects tab
        
    #----------------------------------------------------------------------
    def SetToRecipes(self, id):
        self.recipeBook.ChangeActiveDataItem(id) #Load recipe 'id'
        self.recipeBook.SetSelection(0)          #Set to overview tab
        self.SetSelection(3)                     #Switch to recipes tab
       
