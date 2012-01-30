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

import math

###############################################################################
class Hop(object):
    """ Class to describe hops and their properties """
    #-------------------------------------------------------------------------
    def __init__(self, name, quantity, boiltime, aau, form):
        self.name = name
        self.amount = quantity
        self.boiltime = boiltime
        self.aau = aau
        self.form = form
        
        #Calculated values
        self.use = 0
        self.IBU = 0
        
        
    #-------------------------------------------------------------------------
    def GetColStrings(self):
        return [str(self.amount.Value('ounces')),
                '%3.0f' % self.boiltime,
                '%3.1f' % self.aau,
                self.form,
                '%2.0f' % self.use,
                '%2.0f' % self.IBU]
    
    #-------------------------------------------------------------------------
    def calcUse(self, method, boilOG):
        """ Calculate a hop's use percentage """
        if (self.amount.Value('ounces') != 0. and 
            self.boiltime != 0. and 
            self.aau != 0.):
            if method == 'Daniels':
                self.use = (round(-0.0051 * self.boiltime**2. + 
                                  0.7835*self.boiltime + 1.9348, 0) 
                            if self.form == 'Pellets'
                            else round(-0.0041 * self.boiltime**2. + 
                                       0.6261*self.boiltime + 1.5779, 0))
            elif method == 'Rager':
                Z = 1.0 if self.form == 'Pellets' else 0.9
                X = (self.boiltime - 31.322749) / 18.267743
                Y = (math.exp(2.*X) - 1.) / (math.exp(2.*X) + 1.)
                self.use = round( (18.109069 + 13.862036*Y) * Z, 0)
            elif method == 'Tinseth':
                Z = 1.1 if self.form == 'Pellets' else 1.0
                self.use = round(1.65 * 0.000125**(boilOG - 1.) * 
                                 (1. - math.exp(-0.04*self.boiltime)) / 
                                 4.15 * 100. * Z, 0)
            elif method == 'Garetz':
                Z = 1.0 if self.form == 'Pellets' else 0.9
                X = (self.boiltime - 21.86) / 24.71
                Y = (math.exp(2.*X) - 1.) / (math.exp(2.*X) + 1.)
                self.use = max([round( (7.2994 + 15.0746*Y) * Z, 0), 0])

    #-------------------------------------------------------------------------
    def calcIBU(self, method, totalSize, batchSize, OG):
        """ Calculate a hop's IBU contribution """
        if totalSize > 0. and batchSize > 0.:
            if method == 'Daniels' or method == 'Garetz':
                self.IBU = round(0.7489 * self.amount.Value('ounces') * 
                                 self.aau * self.use / (totalSize * 
                                 (1. + (OG-1.05)/0.2)), 0)
            elif method == 'Rager':
                self.IBU = (round(0.7489 * self.amount.Value('ounces') * 
                                 self.aau * self.use / (totalSize * (1. + 
                                 (OG-1.05)/0.2)), 0)
                           if OG > 1.051 
                           else round(0.7489 * self.amount.Value('ounces') * 
                                      self.aau * self.use / totalSize, 0))
            elif method == 'Tinseth':
                self.IBU = round(0.7489 * self.amount.Value('ounces') * 
                                 self.aau * self.use / totalSize, 0)
        else:
            self.IBU = 0
        return self.IBU

    #-------------------------------------------------------------------------
    def __eq__(self, other):
        """ Define the hop equality operator """
        return (self.name == other.name and
                self.amount == other.amount and
                self.boiltime == other.boiltime and
                self.aau == other.aau and
                self.form == other.form)

    #-------------------------------------------------------------------------
    def __ne__(self, other):
        """ Define the hop inequality operator """
        return not self.__eq__(other)
