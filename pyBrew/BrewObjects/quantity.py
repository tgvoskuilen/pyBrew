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
    
###############################################################################
class Quantity(object):
    unitDict = {'pounds' : [1, 'weight', 'lb'],
                'ounces' : [16, 'weight', 'oz'],
                'cups' : [1, 'volume', 'c'],
                'tablespoons' : [16, 'volume', 'T'],
                '' : [1,'counting', ''],
                'packet' : [1, 'counting', 'pack']}
                
    WeightUnits = ['pounds','ounces'] #TODO: derive from unitDict
    AllUnits = unitDict.keys()
    
    #-------------------------------------------------------------------------            
    def __init__(self, value, unit):
        try:
            conversion = self.unitDict[unit][0]
            self._unitType = self.unitDict[unit][1]
        except KeyError:
            print "Error: '%s' is not a valid unit" % unit
            raise UnitException("Invalid unit in Quantity initialization")
            
        if type(value) != type(float()) or type(value) != type(int()):
            try:
                value = float(value)
            except:
                raise UnitException("Input quantity is not a number")
                
        self._unit = unit
        self._value = value / conversion
        
    #-------------------------------------------------------------------------
    def Scale(self, scale_factor):
        self._value *= scale_factor
        #TODO: Make this generally applicable to all units in unitDict
        if self._unitType == 'weight':
            if self._unit == 'pounds' and self._value < 0.9:
                self._unit = 'ounces'
            if self._unit == 'ounces' and self._value > 1.1:
                self._unit = 'pounds'
        elif self._unitType == 'volume':
            pass
            
    #-------------------------------------------------------------------------
    def Value(self, unit='default'):
        if unit == 'default':
            unit = self._unit
        try:
            if self._unitType != self.unitDict[unit][1]:
                raise UnitException("Invalid unit type in Quantity Value() method")
                
            #TODO Add functionality for counting unit representation to nearest
            #integer here?
            return self._value * self.unitDict[unit][0]
        except KeyError:
            raise UnitException("invalid unit")
        
    #-------------------------------------------------------------------------
    def Unit(self):
        return self._unit
        
    #-------------------------------------------------------------------------
    def UnitShort(self):
        return self.unitDict[self._unit][2]
        
    #-------------------------------------------------------------------------
    def __eq__(self, other):
        """ Define the quantity equality operator """
        if self._unitType == other._unitType and self._value == other._value:
            return True
        else:
            return False

    #-------------------------------------------------------------------------
    def __ne__(self, other):
        """ Define the quantity inequality operator """
        return not self.__eq__(other)
        
        
###############################################################################
class UnitException(Exception):
    def _get_message(self):
        return self._message
    def _set_message(self, message):
        self._message = message
    message = property(_get_message, _set_message)
