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
import os
import string
import pyBrew.BrewData

###############################################################################
class ImportError(wx.MessageDialog):
    """ Alert user if import fails """
    #----------------------------------------------------------------------
    def __init__(self, filename, type):
        wx.MessageDialog.__init__(self, None, 
            'The file "'+filename+'" could not be imported as a '+
            string.lower(type)+'.','Import Error', wx.OK|wx.ICON_ERROR)
            

###############################################################################
class SaveMessage(wx.MessageDialog):
    """ Ask to save data or not """
    #----------------------------------------------------------------------
    def __init__(self, text):
        wx.MessageDialog.__init__(self, None, 'Save changes to "'+text+'"?',
            'Save Changes?', wx.YES_NO|wx.CANCEL|wx.YES_DEFAULT|wx.ICON_QUESTION)
            
            
###############################################################################
class ConfirmDelete(wx.MessageDialog):
    """ Confirm delete of project or recipe """
    #----------------------------------------------------------------------
    def __init__(self, text):
        wx.MessageDialog.__init__(self,None,'Are you sure you want to delete "'
            +text+'"?\n This action cannot be undone.',
            'Delete?', wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
            
            
###############################################################################
class About(wx.Dialog):
    """ Show info about the program """
    #----------------------------------------------------------------------
    def __init__(self, parent):
                 
        wx.Dialog.__init__(self, parent, wx.ID_ANY, 'About')
        
        lines = []
        lines.append(wx.StaticText(self,-1,'This is pyBrew Version 1.1'))
        lines.append(wx.StaticText(self,-1,'Created by Tyler Voskuilen'))
        lines.append(wx.StaticText(self,-1,'Copyright 2011'))
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.AddSpacer((-1,50))
        for line in lines:
            vBox.Add(line, 0, wx.LEFT|wx.RIGHT, 50)
        vBox.AddSpacer((-1,50))
        self.SetSizer(vBox)
        vBox.Fit(self)
        
    

###############################################################################
class GetFilePath(wx.FileDialog):
    """ Get path for imports or exports """
    #----------------------------------------------------------------------
    def __init__(self, parent, type='Project', mode='Import'):
    
        wildcard = "CSV Files (*.csv)|*.csv"
        
        currentDir = os.getcwd()
        
        style = wx.OPEN if mode == 'Import' else wx.SAVE|wx.OVERWRITE_PROMPT
        
        wx.FileDialog.__init__(self, parent, mode+' '+type, wildcard=wildcard,
                               defaultDir=currentDir+'/UserData', style=style)

        

###############################################################################
class ModifyTopItems(wx.Dialog):
    """ Add/Remove projects and recipes """
    #----------------------------------------------------------------------
    def __init__(self, parent, action='New', type='Project'):
    
        wx.Dialog.__init__(self, parent, wx.ID_ANY, action + ' ' + type, 
                           size=(-1,-1))

        #Make Items
        if action == 'New':
            label = wx.StaticText(self, -1, 'Name')
            self.text = wx.TextCtrl(self, -1, 'New '+type, size=(300,-1))
            self.ok = wx.Button(self, wx.ID_OK, 'Add')
        else:
            label = wx.StaticText(self, -1, 'Select '+type)
            choices = (parent.data.getProjectNames() if type == 'Project'
                       else parent.data.getRecipeNames())
            self.text = wx.ComboBox(self, -1, choices=choices, 
                                    style=wx.CB_READONLY, size=(300,-1))
            self.text.SetSelection(0)
            self.ok = wx.Button(self, wx.ID_OK, action)
            
        self.cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel')

        #Layout items
        vBox =  wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)

        hBox1.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        hBox1.Add(self.text, 1, wx.EXPAND|wx.ALL, 5)
        
        hBox2.Add(self.ok, 1, wx.EXPAND|wx.ALL, 5)
        hBox2.Add(self.cancel, 1, wx.EXPAND|wx.ALL, 5)

        vBox.Add(hBox1, 0, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox2, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(vBox)
        vBox.Fit(self)
