
import wx

###############################################################################
class Styles(wx.Panel):
    """
    This is the main project panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        txt = wx.StaticText(self,-1,'The Styles explorer is not yet implemented.')
 
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(txt, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(vBox)
        
    def LoadActivePanel(self):
        pass
