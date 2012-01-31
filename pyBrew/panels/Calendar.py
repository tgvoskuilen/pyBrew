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
import wx.lib.calendar as LC

###############################################################################
class Calendar(wx.Panel):
    """
    This is the main project panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.calendar = LC.Calendar(self, -1, size=(500,400))
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(self.calendar, 1, wx.EXPAND|wx.ALL, 10)
        
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.year_txt = wx.StaticText(self, -1, 'Year')
        self.month_txt = wx.StaticText(self, -1, 'Month')
        self.spin_year = wx.SpinCtrl(self, -1, size=(100,-1))
        self.spin_month = wx.SpinCtrl(self, -1, size=(100,-1))
        
        #hBox.AddSpacer((20,-1), 1)
        hBox.Add(self.month_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        hBox.Add(self.spin_month, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        hBox.Add(self.year_txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        hBox.Add(self.spin_year, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        
        vBox.Add(hBox, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 20)
        
        start_month = self.calendar.GetMonth()
        start_year = self.calendar.GetYear()
        
        self.spin_year.SetRange(1980,start_year+1)
        self.spin_year.SetValue(start_year)
        
        self.spin_month.SetRange(1,12)
        self.spin_month.SetValue(start_month)
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSpinYear, self.spin_year)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpinMonth, self.spin_month)
        self.SetSizer(vBox)
        #Embellish calendar with DC drawing (how to add images?)
        
    def OnSpinYear(self, event):
        self.calendar.SetYear(self.spin_year.GetValue())
        self.calendar.Refresh()

    def OnSpinMonth(self, event):
        self.calendar.SetMonth(self.spin_month.GetValue())
        self.calendar.Refresh()
        

    def LoadActivePanel(self):
        pass
        
###############################################################################
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, "Testing", size=(600,500))
    calander = Calendar(frame)
    frame.Show(True)
    app.MainLoop()
