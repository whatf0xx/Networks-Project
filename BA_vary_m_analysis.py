# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 12:51:08 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("./BA_10_4_av_vary_m.pkl")

m = Data.keys()

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 3, figsize=(7.2, 4.8))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

for e, mi in enumerate(m):
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    
    i = int(e/3)
    j = e%3

    ax[i][j].set_xscale("log")
    ax[i][j].set_yscale("log")

    ax[i][j].errorbar(centres, data, yerr = errors,
            color=colors[e], marker='.', linewidth=0, 
            elinewidth=1.0, label=f"$m={mi}$")

ax[1][2].set_visible(False)

fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
fig.text(0.01, 0.5, "Probability density $p_\\infty(k)$", va='center',
         rotation='vertical')
fig.legend(loc=(0.72, 0.11))

fig.tight_layout(pad=0.4, rect=(0.04,0.04,0.96,0.96))

#%%

fig, ax = plt.subplots(2, 3, figsize=(7.2, 4.8))

for e, mi in enumerate(m):
    
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    
    i = int(e/3)
    j = e%3

    ax[i][j].set_xscale("log")
    ax[i][j].set_yscale("log")

    ax[i][j].errorbar(centres, data*centres*(centres+1)*(centres+2), yerr = errors,
            color=colors[e], marker='.', linewidth=0, 
            elinewidth=1.0, label=f"$m={mi}$")

ax[1][2].set_visible(False)

fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
mt = "Modified probability $p_\\infty(k) \\cdot k \\cdot (k+1) \\cdot (K+2)$"
fig.text(0.01, 0.5, mt, va='center',
         rotation='vertical')
fig.legend(loc=(0.72, 0.11))

fig.tight_layout(pad=0.4, rect=(0.04,0.04,0.96,0.96))