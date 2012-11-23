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

import re
         
###############################################################################    
def NumString(num, mode='Dec'):
    """
    Convert a number to a string in:
        Decimal (Dec = 1.5 or 12 (2 significant digits))
        Attenuation (Atten = 71.5)
        Integer (Int = 3)
        Gravity (Gravity = 1.015)
    If the number is invalid or zero (or a gravity of 1) a blank string is
    returned instead.
    """
    if num == 0. or (num <= 1. and mode == 'Gravity'):
        num_string = ''
    else:
        try:
            if mode == 'Dec':
                num_string = ('%2.1f' % num) if num < 10. else ('%2.0f' % num)
            elif mode =='Atten':
                num_string = ('%3.1f' % num)
            elif mode == 'Int':
                num_string = str(int(round(num,0)))
            elif mode == 'Gravity':
                num_string = '%4.3f' % num
        except:
            num_string = ''
    return num_string
    
###############################################################################
def GetFloat(string, default=0.):
    """
    Convert a string back into a number
    """
    try:
        num = float(string)
    except ValueError:
        num = default
    return num
    
###############################################################################
def Mean(tuple):
    return 0.5*(tuple[0] + tuple[1])

###############################################################################
def Mean(x):
    return sum(x)/len(x)

###############################################################################
def SGToBrix(SG):
    #http://www.brewersfriend.com/brix-converter/
    return (((182.4601 * SG -775.6821) * SG +1262.7794) * SG -669.5622)

###############################################################################
def BrixToSG(Brix):
    #http://www.brewersfriend.com/brix-converter/
    return (Brix / (258.6-((Brix / 258.2)*227.1))) + 1.0

###############################################################################
def ReadLine(line, string):
    getParam = re.search(r'('+string+r':) (.+)', line)
    args = getParam.group(2).strip()
    args = args.split(' ')
    num = args[0]
    if len(args)>1:
        unit = " ".join(args[1:])
        return num, unit
    else:
        return num, ''
        
###############################################################################
