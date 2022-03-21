# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 01:20:34 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("Raw_data_for_KS.pkl")

m = 4

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

scale = 1.08
# smax = np.max(data)
# jmax = jmax = np.ceil(np.log(smax)/np.log(scale))
# binedges = m*scale**(np.arange(jmax + 1))
# binedges = np.unique(binedges.astype('uint64'))

# x = (binedges[:-1] * (binedges[1:]-1)) ** 0.5

# y = np.zeros_like(x)
# count = binned_data.copy()
# count = count.astype('float')
# for i in range(len(y)):
#     y[i] = np.sum(count[binedges[i]:binedges[i+1]]/(binedges[i+1] - binedges[i]))
#     #y[i] = np.sum(count[binedges[i]:binedges[i+1]])
    
# x = x[y!=0]
# y = y[y!=0]

# plt.figure()
# plt.plot(x, y, 'b.')
# plt.plot(x, p_inf(x)*np.sum(y)/np.sum(p_inf(x)))
# plt.xscale("log")
# plt.yscale("log")

#%% what about tims method

import importlib
mod = importlib.import_module("logbin2020Tim")

plt.figure()

plt.xscale("log")
plt.yscale("log")

for m in [2, 4, 8, 16, 32]:
    
    data = Data[m]["Raw data"]

    tim, taem = mod.logbin(data, scale)

    theory2 = p_inf(tim)
    theory2 *= np.sum(taem)/np.sum(theory2)

    plt.plot(tim, taem, '.')
    plt.plot(tim, theory2, color='#555555', linestyle='dashed')

    chsq = chisquare(taem, theory2)
    print(chsq)

#%%

# fig, ax = plt.subplots(1, 2, figsize=(5.0, 2.2))
# ax[0].plot(points, binned_data, 'b.', markersize=2.6,
#            label="linear binning")
# ax[0].legend(handletextpad=0.05)
# ax[1].plot(tim, taem, 'g.', markersize=2.6,
#            label="log binning")
# ax[1].legend(handletextpad=0.05)

# ax[0].set_xscale("log")
# ax[0].set_yscale("log")

# ax[1].set_xscale("log")
# ax[1].set_yscale("log")

# fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
# fig.text(0.005, 0.5, "Probability density $p_\\infty(k)$", va='center',
#          rotation='vertical')

# fig.tight_layout(pad=0.2, rect=(0.04,0.04,0.98,0.98))

# fig.savefig("log-binning.eps")