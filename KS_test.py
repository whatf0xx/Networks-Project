# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 01:21:31 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("Raw_data_for_KS.pkl")

m = 2

def BA_CDF(k):
    return 1 - m*(m+1)/(k+1)/(k+2)

import numpy as np

data = Data[m]["Raw data"]
normalisation = len(data)

slice1 = 0
slice2 = -1

binned_data = np.bincount(data)[m:]/normalisation
cdf = np.cumsum(binned_data)
points = np.arange(m, len(binned_data)+m, 1)
points = points[slice1:slice2]
cdf = cdf[slice1:slice2]

#for correct normalisation for the p-value
binned_data = binned_data[slice1:slice2]
new_norm = np.sum(binned_data)*normalisation

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt


# plt.plot(binned_data, 'b.')
# plt.xscale("log")
# plt.yscale("log")

plt.figure()
plt.plot(points, cdf, 'b.')
plt.xscale("log")
plt.yscale("log")

plt.plot(points, BA_CDF(points))

diffs = abs(cdf-BA_CDF(points))
loc = np.argmax(diffs)
KS_result = max(abs(cdf-BA_CDF(points)))

from scipy.stats import kstest

theory = BA_CDF(points)

sp_result = kstest(data, BA_CDF)

def p_val(N, D):
    z = np.sqrt(N)*D
    sum = 0
    for i in range(1, 10):
        sum += (-1)**(i+1) * np.exp(-2*(i*z)**2)
    
    return sum

p = p_val(new_norm, KS_result)
print(KS_result)
print(p)

#%%

fig = plt.figure(figsize=(4.8,3.2))
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

plt.plot(points, cdf, 'b.', markersize=3.2, label="Numerical data")

smooth_points = np.logspace(np.log10(m), np.log10(len(binned_data)+m), 1000)
ax.plot(smooth_points, BA_CDF(smooth_points),
        color="green", label="Theory")

ax.set_xlabel("$k$")
ax.set_ylabel("Cumulative distribution function")

ax.legend()

fig.tight_layout(rect=(0,-0.04,0.96,0.98))

fig.savefig("cdf.eps")