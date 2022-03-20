# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 01:21:31 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("Raw_data_for_KS.pkl")

def BA_CDF(m, k):
    return 1 - m*(m+1)/(k+1)/(k+2)

import numpy as np

m = 16

data = Data[m]["Raw data"]
normalisation = 1e6

binned_data = np.bincount(data)[m:]/normalisation
cdf = np.cumsum(binned_data)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

plt.plot(binned_data, 'b.')
plt.xscale("log")
plt.yscale("log")

points = np.arange(m, len(binned_data)+m, 1)

plt.figure()
plt.plot(cdf, 'b.')
#plt.xscale("log")
#plt.yscale("log")

plt.plot(BA_CDF(m, points))

KS_result = max(abs(cdf-BA_CDF(m, points)))

def p_val(N, D):
    z = np.sqrt(N)*D
    sum = 0
    for i in range(1, 10):
        sum += (-1)**(i+1) * np.exp(-2*(i*z)**2)
    
    return sum

p = p_val(1e6, KS_result)
print(KS_result)
print(p)