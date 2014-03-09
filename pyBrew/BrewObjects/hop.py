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
    
    # Some correction factor dictionaries
    hopForms = {'Pellets':    1.1,
                'Whole/Leaf': 1.0}
                
    hopContainment = {'Free':       1.0,
                      'Loose Bag':  0.9,
                      'Packed Bag': 0.8}
                
    yeastFloc = {'Slow':    0.95,
                 'Average': 1.0,
                 'Fast':    1.05}
    
    # Lists of valid keys            
    Forms = sorted(hopForms.keys(), key=str.lower)
    
    #----------------------------------------------------------------------
    @classmethod
    def calcTinseth(cls, args):
        """
        Tinseth form, using adjusted Ubt equation from Michael Hall, Zymurgy
        Special 1997 article on IBU calculation.
        """
        Ubt = 25.367715*(1. - math.exp(-0.04*args['Time']))
        
        OGboil = args['Vtot']/args['Vboil']*(args['OG']-1.)+1.
        
        Fbg = 1.65*0.000125**(OGboil-1.)        # Boil gravity correction
        Fhf = cls.hopForms[args['Form']]        # Hop form correction
        Fbp = cls.Fbp(args['Elevation'])        # Elevation correction
        Fhb = cls.hopContainment[args['Containment']]  # Hop bag correction
        Fyf = cls.yeastFloc[args['YeastFloc']]  # Yeast flocculation correction
        
        # Should I include Fhr in Tinseth? Probably not, since his emperical
        # coefficients were fit to actual data without Fhr included.
        U = Ubt * Fbg * Fhf * Fbp * Fhb * Fyf
        IBU = 0.7489*args['Amount']*args['AAU']*U/args['Vtot']
        
        return (IBU, U)
        
    #----------------------------------------------------------------------
    @classmethod
    def calcRager(cls, args):
        """
        Rager form, using tanh fit for utilization
        """
        Ubt = 18.109069 + 13.862036*math.tanh((args['Time'] - 31.322)/18.268)
        
        Fbg = cls.Fbg(args)                     # Boil gravity correction
        Fhf = cls.hopForms[args['Form']]        # Hop form correction
        Fbp = cls.Fbp(args['Elevation'])        # Elevation correction
        Fhb = cls.hopContainment[args['Containment']] # Hop bag correction
        Fyf = cls.yeastFloc[args['YeastFloc']]  # Yeast flocculation correction
        
        Us = Ubt * Fbg * Fhf * Fbp * Fhb * Fyf
        a = args['Vtot']/args['Vboil']/260.
        c = -0.7489*args['Amount']*args['AAU']*Us/args['Vtot']
        
        IBU = (math.sqrt(1. - 4.*a*c) - 1.) / (2.*a)
        
        Fhr = cls.Fhr(args,IBU)
        U = Us*Fhr
                
        return (IBU, U)
        
        
    #----------------------------------------------------------------------
    @classmethod
    def calcGaretz(cls, args):
        """
        Garetz form, using tanh fit for utilization
        """
        Ubt = max(0., 7.2994 + 15.0746*math.tanh((args['Time']-21.86)/24.71))
        
        Fbg = cls.Fbg(args)                     # Boil gravity correction
        
        # Per Hall 1997 Garetz only corrects for hop form for boil times 
        # between 10 and 30 minutes
        if args['Time'] > 10. and args['Time'] < 30.:
            Fhf = cls.hopForms[args['Form']]
        else:
            Fhf = 1.0
            
        Fbp = cls.Fbp(args['Elevation'])        # Elevation correction
        Fhb = cls.hopContainment[args['Containment']] # Hop bag correction
        Fyf = cls.yeastFloc[args['YeastFloc']]  # Yeast flocculation correction
        
        Us = Ubt * Fbg * Fhf * Fbp * Fhb * Fyf
        a = args['Vtot']/args['Vboil']/260.
        c = -0.7489*args['Amount']*args['AAU']*Us/args['Vtot']
        
        IBU = (math.sqrt(1. - 4.*a*c) - 1.) / (2.*a)
        
        Fhr = cls.Fhr(args,IBU)
        U = Us*Fhr
        
        return (IBU, U)
        
    #----------------------------------------------------------------------
    @classmethod
    def calcDaniels(cls, args):
        """
        Daniels form, reference for quadratic utilization fit unknown
        """
        Ubt = -0.0041 * args['Time']**2. + 0.6261*args['Time'] + 1.5779
        
        Fbg = cls.Fbg(args)                     # Boil gravity correction
        Fhf = cls.hopForms[args['Form']]        # Hop form correction
        Fbp = cls.Fbp(args['Elevation'])        # Elevation correction
        Fhb = cls.hopContainment[args['Containment']] # Hop bag correction
        Fyf = cls.yeastFloc[args['YeastFloc']]  # Yeast flocculation correction
        
        Us = Ubt * Fbg * Fhf * Fbp * Fhb * Fyf
        a = args['Vtot']/args['Vboil']/260.
        c = -0.7489*args['Amount']*args['AAU']*Us/args['Vtot']
        
        IBU = (math.sqrt(1. - 4.*a*c) - 1.) / (2.*a)
        
        Fhr = cls.Fhr(args,IBU)
        U = Us*Fhr
        
        return (IBU, U)
        
    #----------------------------------------------------------------------
    @classmethod
    def Fbg(cls, args):
        """ 
        Standard boil gravity correction (for Rager, Garetz, and Daniels) 
        """
        OGboil = max(1.050, args['Vtot']/args['Vboil']*(args['OG']-1.)+1.)
        return 1./((OGboil-1.050)/0.2 + 1.)
    
    
    #----------------------------------------------------------------------
    @classmethod
    def Fbp(cls, elev):
        """ 
        Correction for boiling temperature changes due to elevation
        """
        return 1./(1. + elev/27500.)
                    
    #----------------------------------------------------------------------
    @classmethod
    def Fhr(cls, args, IBU):
        """ 
        Hop rate factor, from Hall 1997
        """
        return 1. / (1. + args['Vtot']/args['Vboil']*IBU/260.)
        
        
    
    
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
    def calcIBU(self, method, totalVol, boilVol, OG):
        """ 
        Calculate a hop's utilization and IBU contribution, returning IBU
        """
        if totalVol > 0. and boilVol > 0.:
        
            (self.IBU, self.use) = self.hopFormulas[method]\
            (
                {
                    'Amount':      self.amount.Value('ounces'),
                    'AAU':         self.aau, 
                    'Form':        self.form, 
                    'Containment': 'Loose Bag',
                    'YeastFloc':   'Average',
                    'Elevation':   0.,
                    'Time':        self.boiltime,
                    'Vtot':        totalVol, 
                    'Vboil':       boilVol, 
                    'OG':          OG
                }
            )

        else:
            self.IBU = 0
            self.use = 0
            
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
        
        
# Create function map
Hop.hopFormulas = {'Tinseth': Hop.calcTinseth,
                   'Rager':   Hop.calcRager,
                   'Garetz':  Hop.calcGaretz,
                   'Daniels': Hop.calcDaniels}
                   
Hop.FormulaNames = sorted(Hop.hopFormulas.keys(), key=str.lower)
