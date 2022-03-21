# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 14:59:23 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("./BA_N_vary_d1.1.pkl")
m = 3

import numpy as np

N = np.array(list(Data.keys()))

centres = []
val = []
err =[]

for n in N:

    v = Data[n]["Mean degree"]
    print(len(v))
    c = Data[n]["Bin centres"]
    e = Data[n]["Error"]
    
    centres.append(c[v != 0])
    err.append(e[v != 0])
    val.append(v[v != 0])
    print(len(val[-1]))


def p_inf(k):
    return 2*m*(m+1)/k/(k+1)/(k+2)

theory = p_inf(centres[0])

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for i, n in enumerate(N):

    ax.errorbar(centres[i], val[i], yerr=err[i],
            color = colors[i], marker = '.', linewidth = 0,
            elinewidth = 1.0, label=f"N = {n}")
    
ax.plot(centres[0], theory)

ax.legend()

from scipy.stats import chisquare

theory /= np.sum(theory)/np.sum(val[0])

chsq = chisquare(val[0], theory)

#%%
fig = plt.figure()
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for i, n in enumerate(N):

    ax.errorbar(centres[i]/np.sqrt(n),
                val[i]*centres[i]*(centres[i]+1)*(centres[i]+2), 
                yerr=err[i]*centres[i]*(centres[i]+1)*(centres[i]+2),
            color = colors[i], marker = '.', linewidth = 0,
            elinewidth = 1.0, label=f"N = {n}")
    
ax.legend()