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
import pyBrew.dialogs

###############################################################################
class ListPane(wx.Panel):
    def __init__(self, parent, cols, listDialogs, size, dlgTitles):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.list = wx.ListCtrl(self, id=wx.ID_ANY, size=size,
                               style=wx.LC_REPORT|wx.BORDER_SUNKEN)

        self.cols = cols
        self.dataLists = None
        self.listDialogs = listDialogs
        self.dialogTitles = dlgTitles
        self.parent = parent
        
        for col in cols:
            self.list.InsertColumn(col[0], col[1], width=col[2])
            
        #Make 1 add button per entry in dlgTitles
        if len(dlgTitles) == 1:
            bw = 100
            self.adds = [wx.Button(self, -1, 'Add', size=(bw, 30))]
            self.edit = wx.Button(self, -1, 'Edit', size=(bw, 30))
        else:
            bw = 120
            self.adds = []
            for dlg in dlgTitles:
                self.adds.append(wx.Button(self, -1, dlg, size=(bw, 30)))
        
        self.remove = wx.Button(self, -1, 'Remove', size=(bw, 30))
        
        #Organize Layout
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBoxes = []
        props = []

        #Main List
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.list, 1, wx.EXPAND|wx.ALL, 10)
        props.append(1)

        #Button row
        if len(dlgTitles) == 1:
            hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
            hBoxes[-1].AddSpacer((-1,-1), 1)
            hBoxes[-1].Add(self.adds[0], 0, wx.LEFT|wx.BOTTOM, 10)
            hBoxes[-1].Add(self.remove, 0, wx.LEFT|wx.BOTTOM, 10)
            hBoxes[-1].Add(self.edit, 0, wx.LEFT|wx.BOTTOM|wx.RIGHT, 10)
            props.append(0)
        else:
            buttonLabel = wx.StaticText(self, -1, 'Add Items')
            vBox1 = wx.BoxSizer(wx.VERTICAL)
            vBox1.Add(buttonLabel, 0, wx.ALL|wx.ALIGN_CENTER, 5)
            for add in self.adds:
                vBox1.Add(add, 0, wx.ALL, 5)
            vBox1.Add(self.remove, 0, wx.ALL, 5)
            hBoxes[-1].Add(vBox1, 0, wx.ALL, 0)

        #Add all hBoxes to vBox
        for index, hBox in enumerate(hBoxes):
            vBox.Add(hBox, props[index], wx.EXPAND)

        self.SetSizer(vBox)

        #Button bindings
        for index, button in enumerate(self.adds):
            button.Bind(wx.EVT_BUTTON, lambda evt, id=index: self.Add(evt, id))
            
        self.Bind(wx.EVT_BUTTON, self.Remove, self.remove)
        if len(dlgTitles) == 1:
            self.Bind(wx.EVT_BUTTON, self.Edit, self.edit)

        #List box bindings
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit, self.list)
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.RemoveKeyPress, self.list)

    def UpdateValues(self):
        if hasattr(self.parent, 'project'):
            self.parent.project.CalcValues()
        self.list.DeleteAllItems()
        self.ids = []
        for li_id, li in enumerate(reversed(self.dataLists)):
            for index, item in enumerate(li):
                entries = item.GetColStrings()
                row = self.list.InsertStringItem(index,item.name)
                self.ids.append((len(self.dataLists)-li_id-1, len(li)-index-1))
                for colID, entry in enumerate(entries):
                    if colID < len(self.cols)-1:
                        self.list.SetStringItem(row,colID+1,entry)
        self.ids.reverse()
        self.parent.UpdateCalcValues()

    def Add(self, event=None, id=0):
        """ Add item to list """
        LD = self.listDialogs[id](self, 1, 'Add '+self.dialogTitles[id])
        retval = LD.ShowModal()
        newItem = LD.GetNewItem()
        if retval == wx.ID_OK and newItem is not None:
            self.dataLists[id].append(newItem)
            self.UpdateValues()
        LD.Destroy()

    def Remove(self, event=None):
        """ Remove selected items from the list """
        if self.list.GetSelectedItemCount() > 0:
            item = self.list.GetFirstSelected()
            while item != -1:
                id, pos = self.ids[item]
                del self.dataLists[id][pos]
                item = self.list.GetNextSelected(item)
            self.UpdateValues()

    def Edit(self, event=None):
        if self.list.GetSelectedItemCount() == 1:
            item = self.list.GetFirstSelected()
            id, pos = self.ids[item]
            LD = self.listDialogs[id](self, 1, 'Edit '+self.dialogTitles[id], 
                                      self.dataLists[id][pos],'Update')
            retval = LD.ShowModal()
            newItem = LD.GetNewItem()
            if retval == wx.ID_OK and newItem is not None:
                self.dataLists[id][pos] = newItem
                self.UpdateValues()
            LD.Destroy()

    def RemoveKeyPress(self, event):
        """ Remove item from list when delete key is pressed """
        if event.GetKeyCode() == wx.WXK_DELETE:
            self.Remove()
        else:
            event.Skip()
            
