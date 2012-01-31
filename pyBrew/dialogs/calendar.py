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
import wx.calendar as cal

###############################################################################
class Calendar(wx.Dialog):
    """
    Small popup calendar widget to get the date string for a text box
    """
    def __init__(self, parent, id, title, dest):
        wx.Dialog.__init__(self, parent, id, title)
        self.dest = dest
        vbox = wx.BoxSizer(wx.VERTICAL)

        calend = cal.CalendarCtrl(self, -1, wx.DateTime_Now(),
            style = cal.CAL_SHOW_HOLIDAYS|cal.CAL_SEQUENTIAL_MONTH_SELECTION)
        vbox.Add(calend, 0, wx.EXPAND | wx.ALL, 5)

        self.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnCalChange, id=calend.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.SetSizerAndFit(vbox)

    def OnCalChange(self, event):
        date = event.GetDate()
        dt = str(date).split(' ')
        s = '%s %s, %s' % (dt[2], dt[1], dt[3])
        self.dest.SetValue(s)
        
    def OnQuit(self, event):
        self.Destroy()
