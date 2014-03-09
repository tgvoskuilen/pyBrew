"""
Copyright (c) 2014, Tyler Voskuilen
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
import math

from pyBrew.pyBrewMethods import *

###############################################################################
class FGCalculatorDialog(wx.Dialog):
    """ Final gravity refractometer calculator dialog window """
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


###############################################################################
class KegCalculatorDialog(wx.Dialog):
    """ Kegging calculator dialog window """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           title='Kegging Calculator', size=(650,400))

        
        calcColor = (200,200,200)

        self.co2tank = wx.StaticBitmap\
            (
                self, 
                wx.ID_ANY, 
                wx.Bitmap\
                (
                    os.path.join('pyBrew','icons','diagram.png'), 
                    wx.BITMAP_TYPE_ANY
                ),
                pos=(0,10)
            )


        #Make Items
        self.pressure = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_CENTER, 
                                    value='', pos=(140,180),size=(90,-1))
            
            
        self.temperature = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTER, value='40', 
                                    pos=(255,300),size=(90,-1))
        self.co2volumes = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTER, value='2', 
                                    pos=(255,350),size=(90,-1))
                                    
        self.lineLength = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_CENTER, 
                                    value='', pos=(360,90),size=(70,-1))
        self.lineID = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTER, value='3/16', 
                                    pos=(360,140),size=(70,-1))
        self.faucetH = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTER, value='1.5', 
                                    pos=(360,190),size=(70,-1))
                                    
                                    
        self.faucetP = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTER, value='2', 
                                    pos=(500,230),size=(60,-1))                   
        self.fillTime = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_CENTER, value='10', 
                                    pos=(500,280),size=(60,-1))

        unitBox = wx.StaticBox(self, -1, 'Select Units:',size=(110,80),pos=(10,310))

        self.selectEng = wx.RadioButton(self, -1, 'English',pos=(20,330), style=wx.RB_GROUP)
        self.selectMetric = wx.RadioButton(self, -1, 'Metric',pos=(20,360))
        
        
        self.exitButton = wx.Button(self, wx.ID_CANCEL, 'Exit', pos=(550,360), size=(95,35))
        self.lineLength.SetBackgroundColour(calcColor)
        self.pressure.SetBackgroundColour(calcColor)


        #Make Labels
        wx.StaticText(self, -1, label='Set Pressure', size=(100,-1), pos=(140,160))
        
        self.IDlabel = wx.StaticText(self, -1, label='Line ID (in)', size=(100,-1), pos=(360,120))
        wx.StaticText(self, -1, label='Line Length', size=(100,-1), pos=(360,70))
        
        self.faucetHLabel = wx.StaticText(self, -1, label='Faucet Height (ft)', size=(120,-1), pos=(360,170))
     
        self.faucetPLabel = wx.StaticText(self, -1, label='Faucet Loss (psi)', size=(120,-1), pos=(500,210))

        wx.StaticText(self, -1, label='Pint Fill Time (s)', size=(120,-1), pos=(500,260))

        
        self.TLabel = wx.StaticText(self, -1, label='Temperature (F)', size=(150,-1), pos=(255,280))
        wx.StaticText(self, -1, label='Volumes of CO2', size=(150,-1), pos=(255,330))

        #Layout items

        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.temperature)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.co2volumes)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.lineID)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.faucetP)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.faucetH)
        self.Bind(wx.EVT_TEXT, self.UpdateValues,  self.fillTime)
        
        self.Bind(wx.EVT_RADIOBUTTON, self.SetUnits, self.selectEng)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetUnits, self.selectMetric)
        
        self.useMetric = False
        self.UpdateValues()

    # -------------------------------------------------------------------------
    def SetUnits(self, event=None):

        if self.selectEng.GetValue():
            self.IDlabel.SetLabel('Line ID (in)')
            self.faucetHLabel.SetLabel('Faucet Height (ft)')
            self.faucetPLabel.SetLabel('Faucet Loss (psi)')
            self.TLabel.SetLabel('Temperature (F)')
            
            self.useMetric = False
            
            values = self.ReadInputs()
            values['T'] = 1.8*values['T'] + 32.  # convert C to F
            values['ID'] = values['ID']/25.4     # convert mm to in
            values['Pf'] = values['Pf']*14.504   # convert bar to psi
            values['H'] = values['H']*3.28       # convert m to ft
            
            # Write converted values
            self.temperature.SetValue('%2.0f' % values['T'])
            self.lineID.SetValue('%4.3f' % values['ID'])
            self.faucetP.SetValue('%2.0f' % values['Pf'])
            self.faucetH.SetValue('%3.1f' % values['H'])
            
        else:
            self.IDlabel.SetLabel('Line ID (mm)')
            self.faucetHLabel.SetLabel('Faucet Height (m)')
            self.faucetPLabel.SetLabel('Faucet Loss (bar)')
            self.TLabel.SetLabel('Temperature (C)')
            
            self.useMetric = True
            
            values = self.ReadInputs()
            values['T'] = (values['T'] - 32.)/1.8 # convert F to C
            values['ID'] = values['ID']*25.4      # convert in to mm
            values['Pf'] = values['Pf']/14.504    # convert psi to bar
            values['H'] = values['H']/3.28        # convert ft to m
            
            # Write converted values
            self.temperature.SetValue('%2.0f' % values['T'])
            self.lineID.SetValue('%4.1f' % values['ID'])
            self.faucetP.SetValue('%4.2f' % values['Pf'])
            self.faucetH.SetValue('%3.2f' % values['H'])
            
        self.UpdateValues(event)
    
    # -------------------------------------------------------------------------
    def ReadInputs(self):
    
        T = GetFloat(self.temperature.GetValue(),-1.)
        V = GetFloat(self.co2volumes.GetValue(),-1.)
        IDstr = self.lineID.GetValue()
        Pf = GetFloat(self.faucetP.GetValue(),-1.)
        time = GetFloat(self.fillTime.GetValue(),-1.)
        height = GetFloat(self.faucetH.GetValue(),-1.)
        
        inputs = {}
        
        if T > 0. and V > 0. and Pf > 0. and time > 0. and height > 0.:
            # attempt to read IDstr
            
            try:
                ID = float(IDstr)
            except ValueError:
                # try to make fraction
                try:
                    parts = [float(x) for x in IDstr.split('/')]
                    ID = parts[0]/parts[1]
                except ValueError:
                    ID = -1.
                    
            if ID > 0.:
                return {'T':T, 'V':V, 'ID':ID, 'Pf':Pf, 't':time, 'H':height}
                
        
        return None
            
    
    # -------------------------------------------------------------------------
    def UpdateValues(self, event=None):
    
        inputs = self.ReadInputs()

        if inputs is None:
            return
            
        # Proceed with calculation since inputs are ok
        if self.useMetric:
            Tf = 1.8*inputs['T'] + 32.
        else:
            Tf = inputs['T']
            
        V = inputs['V']
        
        P = -16.6999 - (0.0101059 * Tf) + (0.00116512 * Tf**2.) + \
                (0.173354 * Tf * V) + (4.24267 * V) - (0.0684226 * V**2.)
        
        if self.useMetric:
            P = P / 14.504
        
        if P > 0.:
            if self.useMetric:
                self.pressure.ChangeValue('%4.2f bar' % P)
            else:
                self.pressure.ChangeValue('%3.1f psig' % P)
        else:
            self.pressure.ChangeValue('')

        # Calculate line length now
        
        # Common online correlations use too large a value of flow resistance

        
        # Some constants
        nu = 1.5e-6  # m^2/s
        rho = 1010.  # kg/m^3
        e = 5e-6     # m, vinyl hose surface roughness
        
        
        # Convert ID and H to meters
        ID = inputs['ID']
        H = inputs['H']
        
        if not self.useMetric:
            ID = ID*2.54/100.
            H = H / 3.28
        else:
            ID = ID/1000.
        
        # Flow rate
        Q = 1./(inputs['t']*2113.38)  # m^3/s
        v = 4.*Q/(math.pi*ID**2.)  # m/s
        
        Re = v*ID/nu
        
        # Friction factor - Swamee-Jain approx. of Colebrook
        f = 0.25*(math.log10(e/(3.7*ID) + 5.74/Re**0.9))**-2.
        
        
        R_line = 0.5*rho*v**2.*f/ID  # Pa/m
        DP_gravity = rho*9.81*H      # Pa
        
        if not self.useMetric:
            R_line = R_line / 6894.8 / 3.28  # to psi/ft
            DP_gravity = DP_gravity / 6894.8 # psi
        else:
            R_line = R_line/1e5  # bar/m
            DP_gravity = DP_gravity/1e5  # bar
        
        L_line = (P - inputs['Pf'] - DP_gravity)/R_line  # ft or m
        
        if L_line > 0.:
            unitstr = 'm' if self.useMetric else 'ft'
            self.lineLength.ChangeValue('%2.1f %s' % (L_line,unitstr))
        else:
            self.lineLength.ChangeValue('')


