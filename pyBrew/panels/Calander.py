
import wx
import wx.lib.calendar as LC

###############################################################################
class Calander(wx.Panel):
    """
    This is the main project panel
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.calendar = LC.Calendar(self, -1, size=(500,400))
        
        #Embellish calendar with DC drawing (how to add images?)
        
    def LoadActivePanel(self):
        pass
        
###############################################################################
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, "Testing", size=(600,500))
    calander = Calander(frame)
    frame.Show(True)
    app.MainLoop()