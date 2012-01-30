
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
        txt = wx.StaticText(self,-1,'Styles View')
 
    def LoadActivePanel(self):
        pass