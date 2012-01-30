
import wx
import pyBrew.BrewData
import pyBrew.Databases

###############################################################################
class AddYeastDialog(wx.Dialog):
    """ Add/Edit yeast item dialog window """
    #----------------------------------------------------------------------
    def __init__(self, parent, id, title, inputYeast=pyBrew.BrewData.Yeast(''),
                 okButtonText='Add'):
        wx.Dialog.__init__(self, parent, id, title, size=(450,500))

        #Make Items
        self.yeastSelect = wx.ComboBox(self, -1, 
            choices=pyBrew.Databases.YeastDb.Names,
            style=wx.CB_READONLY, size=(350,-1))
        self.okButton = wx.Button(self, wx.ID_OK, okButtonText)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        
        desclabel = wx.StaticBox(self, -1, 'Description', size=(400,350))
        boxsizer = wx.StaticBoxSizer(desclabel, wx.VERTICAL)
        self.yeastDesc  = wx.StaticText(self,-1,'',(400,350))
        self.yeastDesc.Wrap(400)
        boxsizer.Add(self.yeastDesc, 1, wx.ALL|wx.EXPAND, 5)
        desclabel.SetFont(wx.Font(pointSize=11,
                          family=wx.FONTFAMILY_DEFAULT,
                          weight=wx.FONTWEIGHT_BOLD,
                          style=wx.FONTSTYLE_NORMAL))
                                  
        #Set Value
        self.yeastSelect.SetSelection(
            pyBrew.Databases.YeastDb.GetID(inputYeast.name))
        
        #Make Labels
        yeastLabel = wx.StaticText(self, -1, label='Yeast Type:')

        #Layout items
        self.vBox =  wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)
        hBox4 = wx.BoxSizer(wx.HORIZONTAL)

        hBox1.Add(yeastLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        hBox1.Add(self.yeastSelect, 1, wx.EXPAND|wx.ALL, 5)
        
        hBox3.Add(boxsizer, 1, wx.ALL, 5)

        hBox4.Add(self.okButton, 1, wx.EXPAND|wx.ALL, 5)
        hBox4.Add(self.cancelButton, 1, wx.EXPAND|wx.ALL, 5)

        self.vBox.Add(hBox1, 0, wx.EXPAND|wx.ALL, 5)
        self.vBox.Add(hBox2, 0, wx.EXPAND|wx.ALL, 5)
        self.vBox.Add(hBox3, 1, wx.EXPAND|wx.ALL, 5)
        self.vBox.Add(hBox4, 0, wx.EXPAND|wx.ALL, 5)
        
        self.Bind(wx.EVT_COMBOBOX, self.UpdateDescription, self.yeastSelect)

        self.SetSizer(self.vBox)
        #self.vBox.Fit(self)
        self.UpdateDescription()
        
    #----------------------------------------------------------------------
    def UpdateDescription(self, event=None):
        desc = pyBrew.Databases.YeastDb.Description(self.yeastSelect.GetValue())
        self.yeastDesc.SetLabel(desc)
        self.yeastDesc.Wrap(400)
        #self.Layout()
            
    #----------------------------------------------------------------------
    def GetNewItem(self):
        if self.yeastSelect.GetSelection() >= 0:
            return pyBrew.BrewData.Yeast(self.yeastSelect.GetValue())
        else:
            return None

        