
###############################################################################
class Other:
    """ Class to describe other ingredients and their properties """
    #-------------------------------------------------------------------------
    def __init__(self, name, quantity):
        self.name = name
        self.amount = quantity
        
    #-------------------------------------------------------------------------
    def __eq__(self, rhs):
        """ Define the other item equality operator """
        if self.name == rhs.name and self.amount == rhs.amount:
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def __ne__(self, rhs):
        """ Define the other item inequality operator """
        return not self.__eq__(rhs)
        
    #-------------------------------------------------------------------------
    def GetColStrings(self):
        return [str(self.amount.Value())+'  '+self.amount.UnitShort()]
