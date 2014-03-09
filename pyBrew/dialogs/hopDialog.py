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
class AddHopDialog(wx.Dialog):
    """ Add/edit hops in Project Window """
    #----------------------------------------------------------------------
    def __init__(self, parent, id, title, inputHop=pyBrew.BrewObjects.Hop('', 
                    pyBrew.BrewObjects.Quantity(0,'ounces'), 0, 0, 'Pellets'),
                 okButtonText='Add'):
                 
        wx.Dialog.__init__(self, parent, id, title, size=(-1,-1))

        #Make Items
        self.hopSelect = wx.ComboBox(self, -1,
            choices=pyBrew.Databases.HopDb.Names,
            style=wx.CB_READONLY, size=(250,-1))
        self.hopAmount = wx.TextCtrl(self, -1, value='')
        self.hopBoilTime = wx.TextCtrl(self, -1, value='')
        self.hopAAU = wx.TextCtrl(self, -1, value='')
        self.hopForm = wx.ComboBox(self, -1,
            choices=pyBrew.BrewObjects.Hop.Forms,
            style=wx.CB_READONLY)
        self.okButton = wx.Button(self, wx.ID_OK, okButtonText)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, 'Cancel')

        #set inputs
        amt = str(inputHop.amount.Value('ounces')) \
            if inputHop.amount.Value() > 0. else ''
        boilTime = str(inputHop.boiltime) if inputHop.boiltime > 0 else ''
        aau = str(inputHop.aau) if inputHop.aau > 0 else ''
            
        try:
            form_id = pyBrew.BrewObjects.Hop.Forms.index(inputHop.form)
        except ValueError:
            form_id = 0 #Default to pellets
        
        self.hopSelect.SetSelection(
            pyBrew.Databases.HopDb.GetID(inputHop.name))
        self.hopAmount.SetValue(amt)
        self.hopBoilTime.SetValue(boilTime)
        self.hopAAU.SetValue(aau)
        self.hopForm.SetSelection(form_id)

        #Make Labels
        hopLabel = wx.StaticText(self, -1, label='Item:')
        amtLabel = wx.StaticText(self, -1, label='Amount (oz):')
        timeLabel = wx.StaticText(self, -1, label='Boil Time (min):')
        aauLabel = wx.StaticText(self, -1, label='AAU (%):')
        formLabel = wx.StaticText(self, -1, label='Form:')

        #Layout items
        vBox =  wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)
        hBox5 = wx.BoxSizer(wx.HORIZONTAL)
        hBox6 = wx.BoxSizer(wx.HORIZONTAL)

        hBox1.Add(hopLabel, 0, wx.ALL, 5)
        hBox1.Add(self.hopSelect, 1, wx.EXPAND|wx.ALL, 5)

        hBox2.Add(amtLabel, 0, wx.ALL, 5)
        hBox2.Add(self.hopAmount, 1, wx.EXPAND|wx.ALL, 5)

        hBox3.Add(timeLabel, 0, wx.ALL, 5)
        hBox3.Add(self.hopBoilTime, 1, wx.EXPAND|wx.ALL, 5)

        hBox4.Add(aauLabel, 0, wx.ALL, 5)
        hBox4.Add(self.hopAAU, 1, wx.EXPAND|wx.ALL, 5)

        hBox5.Add(formLabel, 0, wx.ALL, 5)
        hBox5.Add(self.hopForm, 1, wx.EXPAND|wx.ALL, 5)

        hBox6.Add(self.okButton, 1, wx.EXPAND|wx.ALL, 5)
        hBox6.Add(self.cancelButton, 1, wx.EXPAND|wx.ALL, 5)

        vBox.Add(hBox1, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox2, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox3, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox4, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox5, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox6, 1, wx.EXPAND|wx.ALL, 5)

        #Bind events to put default AAU value in box when hop is changed
        self.Bind(wx.EVT_COMBOBOX, self.updateAAU, self.hopSelect)
        self.SetSizer(vBox)
        vBox.Fit(self)

    #----------------------------------------------------------------------
    def GetNewItem(self):
        try:
            boilTime = float(self.hopBoilTime.GetValue())
            aau = float(self.hopAAU.GetValue())
            hopAmt = float(self.hopAmount.GetValue())
        except ValueError:
            return None
            
        return pyBrew.BrewObjects.Hop(self.hopSelect.GetValue(),
                   pyBrew.BrewObjects.Quantity(hopAmt,'ounces'),
                   boilTime, aau, self.hopForm.GetValue())

    #----------------------------------------------------------------------
    def updateAAU(self, event):
        self.hopAAU.SetValue('%2.1f' % 
            pyBrew.Databases.HopDb.AAU(self.hopSelect.GetValue()))

