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
import pyBrew.BrewData
import pyBrew.Databases

###############################################################################
# AddOtherDialog - Used to add or edit other ingredients to recipe
#
###############################################################################
class AddOtherDialog(wx.Dialog):
    """ Add/Edit other item dialog window """
    def __init__(self, parent, id, title, inputOther=pyBrew.BrewData.Other('',
                    pyBrew.BrewData.Quantity(0,'')), okButtonText='Add'):
                    
        wx.Dialog.__init__(self, parent, id, title, size=(-1,-1))

        #Make Items
        self.itemName = wx.TextCtrl(self, -1, value='', size=(350,-1))
        self.itemAmount = wx.TextCtrl(self, -1, value='')
        self.itemUnit = wx.ComboBox(self, -1, 
            choices=pyBrew.BrewData.Quantity.AllUnits)
        self.okButton = wx.Button(self, wx.ID_OK, okButtonText)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, 'Cancel')

        #Set Values
        try:
            unit_id = pyBrew.BrewData.Quantity.AllUnits.index(
                            inputOther.amount.Unit())
        except ValueError:
            unit_id = 0
            
        self.itemName.ChangeValue(inputOther.name)
        amt = (str(inputOther.amount.Value()) if 
               inputOther.amount.Value() > 0. else '')
        self.itemAmount.ChangeValue(amt)
        self.itemUnit.SetSelection(unit_id)
        
        #Make Labels
        itemNameLabel = wx.StaticText(self, -1, label='Item:')
        itemAmountLabel = wx.StaticText(self, -1, label='Amount:')

        #Layout items
        vBox =  wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

        hBox1.Add(itemNameLabel, 0, wx.ALL, 5)
        hBox1.Add(self.itemName, 1, wx.EXPAND|wx.ALL, 5)
        
        hBox2.Add(itemAmountLabel, 0, wx.ALL, 5)
        hBox2.Add(self.itemAmount, 1, wx.EXPAND|wx.ALL, 5)
        hBox2.Add(self.itemUnit, 1, wx.EXPAND|wx.ALL, 5)

        hBox3.Add(self.okButton, 1, wx.EXPAND|wx.ALL, 5)
        hBox3.Add(self.cancelButton, 1, wx.EXPAND|wx.ALL, 5)

        vBox.Add(hBox1, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox2, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox3, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(vBox)
        vBox.Fit(self)

    def GetNewItem(self):
        try:
            amt = float(self.itemAmount.GetValue())
        except:
            return None
            
        return pyBrew.BrewData.Other(self.itemName.GetValue(),
                     pyBrew.BrewData.Quantity(amt, self.itemUnit.GetValue()))
        
