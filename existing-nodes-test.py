# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:37:58 2022

@author: whatf0xx
"""

def p_inf(m,k):
    num = (6+9*m) * (4+9*m) * (2+9*m) * (9*m)
    den = 4*(k+4*m+4)*(k+4*m+3)*(k+4*m+2)*(k+4*m+1)*(k+4*m)
    
    return num / den

sum = 0
m = 4

for i in range(int(m/2), int(1e5)):
    sum += i* p_inf(m, i)
    
print(sum)