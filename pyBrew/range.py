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
from pyBrew.pyBrewMethods import NumString

###############################################################################
class Range(object):
    #--------------------------------------------------------------------------
    def __init__(self, vals, rangeMode=False):
        if rangeMode:
            self._mean = 0.5*(vals[0] + vals[1])
            self._err = 0.5*(vals[1] - vals[0])
        else:
            self._mean = vals[0]
            self._err  = vals[1]

    #--------------------------------------------------------------------------
    def __add__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = self._mean + other._mean
        newerr = math.sqrt(self._err**2. + other._err**2.)
        return Range((newmean, newerr))
        
    #--------------------------------------------------------------------------
    def __radd__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = self._mean + other._mean
        newerr = math.sqrt(self._err**2. + other._err**2.)
        return Range((newmean, newerr))
        
    #--------------------------------------------------------------------------
    def __sub__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = self._mean - other._mean
        newerr = math.sqrt(self._err**2. + other._err**2.)
        return Range((newmean, newerr))

    #--------------------------------------------------------------------------
    def __rsub__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = other._mean - self._mean
        newerr = math.sqrt(self._err**2. + other._err**2.)
        return Range((newmean, newerr))
        
    #--------------------------------------------------------------------------
    def __mul__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = self._mean*other._mean
        newerr = math.sqrt((other._mean*self._err)**2. + (self._mean*other._err)**2.)
        return Range((newmean, newerr))
      
    #--------------------------------------------------------------------------
    def __rmul__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = self._mean*other._mean
        newerr = math.sqrt((other._mean*self._err)**2. + (self._mean*other._err)**2.)
        return Range((newmean, newerr))
        
    #--------------------------------------------------------------------------
    def __div__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = float(self._mean)/float(other._mean)
        newerr = math.sqrt((self._err/other._mean)**2. + (self._mean/(other._mean**2.)*other._err)**2.)
        return Range((newmean, newerr))
        
    #--------------------------------------------------------------------------
    def __rdiv__(self, other):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = float(other._mean)/float(self._mean)
        newerr = math.sqrt((other._err/self._mean)**2. + (other._mean/(self._mean**2.)*self._err)**2.)
        return Range((newmean, newerr))

    #--------------------------------------------------------------------------
    def __pow__(self, other):
        """ Pow can handle Range ** Range and Range ** const """
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = self._mean ** other._mean
        newerr = math.sqrt((other._mean * self._mean ** (other._mean - 1.) * self._err)**2. + (math.log(self._mean)*self._mean ** other._mean * other._err)**2.)
        return Range((newmean, newerr))
        
    #--------------------------------------------------------------------------
    def exp(self):
        if not hasattr(other, '_mean'):
            other = Range((other, 0.))
        newmean = math.exp(self._mean)
        newerr = newmean * self._err
        return Range((newmean, newerr))
    
    #--------------------------------------------------------------------------
    def __str__(self):
        return str(self._mean) + ' +/- ' + str(self._err)
        
    #--------------------------------------------------------------------------
    def Format(self, mode='Dec'):
        if self._mean == 0.:
            range_string = ''
        elif self._err == 0.:
            range_string = NumString(self._mean,mode)
        else:
            range_string = NumString(self._mean - self._err,mode)+' - '+ \
                            NumString(self._mean + self._err,mode)
        return range_string
                
