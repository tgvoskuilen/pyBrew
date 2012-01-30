
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
        
        self.SetSizer(vBox)
        #Embellish calendar with DC drawing (how to add images?)
        
    def LoadActivePanel(self):
        pass
        
###############################################################################
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, "Testing", size=(600,500))
    calander = Calendar(frame)
    frame.Show(True)
    app.MainLoop()
