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

from pyBrew.pyBrewMethods import *

###############################################################################
class FGCalculatorDialog(wx.Dialog):
    """ Calculator dialog window """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           title='Refractometer Calculator', size=(-1,-1))

        
        calcColor = (200,200,200)

        #Make Items
        #self.calculateMethod = wx.ComboBox(self, -1,
        #    choices=['Linear','Cubic'],
        #    style=wx.CB_READONLY, size=(150,-1))
        self.measOG = wx.TextCtrl(self, -1, value='', style=wx.TE_CENTER)
        self.measFG = wx.TextCtrl(self, -1, value='', style=wx.TE_CENTER)
        self.calcFG = wx.TextCtrl(self, -1, value='', style=wx.TE_READONLY|wx.TE_CENTER)

        self.exitButton = wx.Button(self, wx.ID_CANCEL, 'Exit')
        self.calcFG.SetBackgroundColour(calcColor)

        #Set Values
        #self.calculateMethod.SetSelection(0)
        
        #Make Labels
        #methodLabel = wx.StaticText(self, -1, label='Calculation Method:', size=(150,-1))
        OGLabel = wx.StaticText(self, -1, label='Measured OG:', size=(150,-1))
        FGLabel = wx.StaticText(self, -1, label='Measured FG:', size=(150,-1))
        FGLabel2 = wx.StaticText(self, -1, label='Calculated FG:', size=(150,-1))

        #Layout items
        hBoxes = []

        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(OGLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        hBoxes[-1].Add(self.measOG, 1, wx.EXPAND|wx.ALL, 5)

        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(FGLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        hBoxes[-1].Add(self.measFG, 1, wx.EXPAND|wx.ALL, 5)

        #hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        #hBoxes[-1].Add(methodLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        #hBoxes[-1].Add(self.calculateMethod, 1, wx.EXPAND|wx.ALL, 5)
        
        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(FGLabel2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        hBoxes[-1].Add(self.calcFG, 1, wx.EXPAND|wx.ALL, 5)

        hBoxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hBoxes[-1].Add(self.exitButton, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5)

        vBox =  wx.BoxSizer(wx.VERTICAL)
        for hBox in hBoxes:
            vBox.Add(hBox, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(vBox)
        vBox.Fit(self)
        
        #self.Bind(wx.EVT_COMBOBOX, self.UpdateValues, self.calculateMethod)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.measOG)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.measFG)

    # -------------------------------------------------------------------------
    def UpdateValues(self, event):
        newOG = GetFloat(self.measOG.GetValue())
        newFG = GetFloat(self.measFG.GetValue())

        #Methods from seanterrill.com, use the mean of the two methods
        factor = 1.040 #wort correction factor
        calcFG = []

        if newOG > 1.0 and newFG > 1.0:
            #Method 1 - SeanTerrill New Linear
            BrixO = SGToBrix(newOG)
            BrixF = SGToBrix(newFG)
            FG = 1.0 - 0.00085683*(BrixO/factor) + 0.0034941*(BrixF/factor)
            calcFG.append(FG)

            #Method 2 - SeanTerrill New Cubic
            FG = (1.0 - 0.0044993*(BrixO/factor)
                      + 0.011774*(BrixF/factor)
                      + 0.00027581*(BrixO/factor)**2
                      - 0.0012717*(BrixF/factor)**2
                      - 0.0000072800*(BrixO/factor)**3
                      + 0.000063293*(BrixF/factor)**3)
            calcFG.append(FG)

            calcFGs = NumString(Mean(calcFG),'Gravity')
        else:
            calcFGs = ''

        self.calcFG.ChangeValue(calcFGs)


