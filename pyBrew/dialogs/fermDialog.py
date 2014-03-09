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
import pyBrew.BrewObjects
import pyBrew.Databases

###############################################################################
class AddFermDialog(wx.Dialog):
    """ Add/Edit fermentable item dialog window """
    #----------------------------------------------------------------------
    def __init__(self, parent, id, title, 
                 inputFerm = pyBrew.BrewObjects.Fermentable('', 
                    pyBrew.BrewObjects.Quantity(0,'pounds')),
                 okButtonText = 'Add'):
                 
        wx.Dialog.__init__(self, parent, id, title, size=(-1,-1))

        #Make Items
        self.fermSelect = wx.ComboBox(self, -1,
            choices=pyBrew.Databases.FermDb.Names,
            style=wx.CB_READONLY, size=(250,-1))
        self.fermAmount = wx.TextCtrl(self, -1, value='')
        self.fermAmountUnit = wx.ComboBox(self, -1,
            choices=pyBrew.BrewObjects.Quantity.WeightUnits,
            style=wx.CB_READONLY, size=(100,-1))
        self.okButton = wx.Button(self, wx.ID_OK, okButtonText)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, 'Cancel')

        #Set Values
        amt = (str(inputFerm.amount.Value()) if inputFerm.amount.Value() > 0.
               else '')
            
        self.fermSelect.SetSelection(
            pyBrew.Databases.FermDb.GetID(inputFerm.name))
        self.fermAmount.SetValue(amt)
        self.fermAmountUnit.SetSelection(
            pyBrew.BrewObjects.Quantity.WeightUnits.index(
                inputFerm.amount.Unit()))
        
        #Make Labels
        fermLabel = wx.StaticText(self, -1, label='Item:')
        amtLabel = wx.StaticText(self, -1, label='Amount:')

        #Layout items
        hBoxes = []

        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(fermLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        hBoxes[-1].Add(self.fermSelect, 1, wx.EXPAND|wx.ALL, 5)

        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(amtLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        hBoxes[-1].Add(self.fermAmount, 1, wx.EXPAND|wx.ALL, 5)
        hBoxes[-1].Add(self.fermAmountUnit, 0, wx.EXPAND|wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        desclabel = wx.StaticBox(self, -1, 'Description')
        boxsizer = wx.StaticBoxSizer(desclabel, wx.VERTICAL)
        self.potential  = wx.StaticText(self,-1,'Potential Gravity: ')
        self.efficiency  = wx.StaticText(self,-1,'Efficiency: ')
        self.srm  = wx.StaticText(self,-1,'SRM Color Units: ')
        boxsizer.Add(self.potential, 1, wx.ALL|wx.EXPAND, 5)
        boxsizer.Add(self.efficiency, 1, wx.ALL|wx.EXPAND, 5)
        boxsizer.Add(self.srm, 1, wx.ALL|wx.EXPAND, 5)
        hBoxes[-1].Add(boxsizer, 1, wx.ALL|wx.EXPAND, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.okButton, 1, wx.EXPAND|wx.ALL, 5)
        hBoxes[-1].Add(self.cancelButton, 1, wx.EXPAND|wx.ALL, 5)

        vBox =  wx.BoxSizer(wx.VERTICAL)
        for hBox in hBoxes:
            vBox.Add(hBox, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(vBox)
        vBox.Fit(self)
        
        self.Bind(wx.EVT_COMBOBOX, self.UpdateSelection, self.fermSelect)
        self.UpdateSelection()

    #----------------------------------------------------------------------
    def GetNewItem(self):
        try:
            fermAmt = float(self.fermAmount.GetValue())
        except:
            return None
            
        return pyBrew.BrewObjects.Fermentable(self.fermSelect.GetValue(),
            pyBrew.BrewObjects.Quantity(fermAmt,self.fermAmountUnit.GetValue()))

    #----------------------------------------------------------------------
    def UpdateSelection(self, event=None):
        self.potential.SetLabel('Potential Gravity: %4.3f' % 
            pyBrew.Databases.FermDb.Potential(self.fermSelect.GetValue()))
        self.efficiency.SetLabel('Efficiency: %3.0f %%' % 
            pyBrew.Databases.FermDb.Efficiency(self.fermSelect.GetValue()))
        self.srm.SetLabel('SRM Color Units: %3.0f' % 
            pyBrew.Databases.FermDb.SRM(self.fermSelect.GetValue()))
