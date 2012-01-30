
import wx
import pyBrew.BrewData
import pyBrew.Databases

###############################################################################
# AddOtherDialog - Used to add or edit other ingredients to recipe
#
###############################################################################
class AddOtherDialog(wx.Dialog):
    """ Add/Edit other item dialog window """
    def __init__(self, parent, id, title, inputOther=pyBrew.BrewData.Other('',
                    pyBrew.BrewData.Quantity(0,'')), okButtonText='Add'):
                    
        wx.Dialog.__init__(self, parent, id, title, size=(-1,-1))

        #Make Items
        self.itemName = wx.TextCtrl(self, -1, value='', size=(350,-1))
        self.itemAmount = wx.TextCtrl(self, -1, value='')
        self.itemUnit = wx.ComboBox(self, -1, 
            choices=pyBrew.BrewData.Quantity.AllUnits)
        self.okButton = wx.Button(self, wx.ID_OK, okButtonText)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, 'Cancel')

        #Set Values
        try:
            unit_id = pyBrew.BrewData.Quantity.AllUnits.index(
                            inputOther.amount.Unit())
        except ValueError:
            unit_id = 0
            
        self.itemName.ChangeValue(inputOther.name)
        amt = (str(inputOther.amount.Value()) if 
               inputOther.amount.Value() > 0. else '')
        self.itemAmount.ChangeValue(amt)
        self.itemUnit.SetSelection(unit_id)
        
        #Make Labels
        itemNameLabel = wx.StaticText(self, -1, label='Item:')
        itemAmountLabel = wx.StaticText(self, -1, label='Amount:')

        #Layout items
        vBox =  wx.BoxSizer(wx.VERTICAL)
        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        hBox3 = wx.BoxSizer(wx.HORIZONTAL)

        hBox1.Add(itemNameLabel, 0, wx.ALL, 5)
        hBox1.Add(self.itemName, 1, wx.EXPAND|wx.ALL, 5)
        
        hBox2.Add(itemAmountLabel, 0, wx.ALL, 5)
        hBox2.Add(self.itemAmount, 1, wx.EXPAND|wx.ALL, 5)
        hBox2.Add(self.itemUnit, 1, wx.EXPAND|wx.ALL, 5)

        hBox3.Add(self.okButton, 1, wx.EXPAND|wx.ALL, 5)
        hBox3.Add(self.cancelButton, 1, wx.EXPAND|wx.ALL, 5)

        vBox.Add(hBox1, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox2, 1, wx.EXPAND|wx.ALL, 5)
        vBox.Add(hBox3, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(vBox)
        vBox.Fit(self)

    def GetNewItem(self):
        try:
            amt = float(self.itemAmount.GetValue())
        except:
            return None
            
        return pyBrew.BrewData.Other(self.itemName.GetValue(),
                     pyBrew.BrewData.Quantity(amt, self.itemUnit.GetValue()))
        
