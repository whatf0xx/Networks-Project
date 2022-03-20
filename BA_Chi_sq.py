# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 01:20:34 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("Raw_data_for_KS.pkl")

m = 16

def p_inf(k):
    return 2*m*(m+1)/k/(k+1)/(k+2)



data = Data[m]["Raw data"]
normalisation = 1e6


import numpy as np

binned_data = np.bincount(data)[m:]
#binned_data = np.append(binned_data, np.zeros(500000))
points = np.arange(m, len(binned_data)+m, 1)
theory = p_inf(points)*normalisation

#%% slicing
# slice1 = 0
# slice2 = -1
# points = points[slice1:slice2]
# binned_data = binned_data[slice1:slice2]
# theory = theory[slice1:slice2]

#%%

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

plt.plot(points, binned_data, 'b.')
plt.plot(points, theory)
plt.xscale("log")
plt.yscale("log")

from scipy.stats import chisquare

theory *= np.sum(binned_data)/np.sum(theory)

chsq = chisquare(binned_data, theory)
print(chsq)

#%% Do we get an improvement for log-binned data?

scale = 1.1
smax = np.max(data)
jmax = jmax = np.ceil(np.log(smax)/np.log(scale))
binedges = m*scale**(np.arange(jmax + 1))
binedges = np.unique(binedges.astype('uint64'))

x = (binedges[:-1] * (binedges[1:]-1)) ** 0.5

y = np.zeros_like(x)
count = binned_data.copy()
count = count.astype('float')
for i in range(len(y)):
    y[i] = np.sum(count[binedges[i]:binedges[i+1]]/(binedges[i+1] - binedges[i]))
    
x = x[y!=0]
y = y[y!=0]

plt.figure()
plt.plot(x, y, 'b.')
plt.plot(x, p_inf(x)*np.sum(y)/np.sum(p_inf(x)))
plt.xscale("log")
plt.yscale("log")