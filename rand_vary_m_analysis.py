# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 12:51:08 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("./rand_vary_m.pkl")

m = Data.keys()

def p_inf(m, k):
    return  (m/(m+1))**(k-m) / (m+1)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

import matplotlib.pyplot as plt

fig = plt.figure(figsize = (5.8,3.8))
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for e, mi in enumerate(m):
    
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    theory = p_inf(mi, centres)
    
    ax.errorbar(centres, data, yerr = errors,
            color=colors[e], marker='.', linewidth=0, 
            elinewidth=1.0,
            zorder = 1, label=f"$m={mi}$")
    
    if e == 0:
        label = "Theoretical value"
    else:
        label = "__nolegend__"
    
    ax.plot(centres, theory,
                  zorder = 2, linestyle="dashed", color="#444444",
                  label = label)
    
ax.set_xlabel("Degree distribution $k$", ha='center')
ax.set_ylabel("Probability density $p_\\infty(k)$")
ax.legend()

fig.tight_layout(rect=(-0.02, -0.04, 0.98, 0.98))
fig.savefig("rand_vary_m.eps")

#%%

import numpy as np

fig = plt.figure(figsize = (5.8,3.6))
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for e, mi in enumerate(m):
    
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    theory = p_inf(mi, centres)
    
    ax.errorbar(centres*(np.log(mi+1)-np.log(mi)), 
                data*(mi/(mi+1))**(mi-centres) * (mi+1), 
                yerr = errors*(mi/(mi+1))**(mi-centres),
                color=colors[e], marker='.', linewidth=0, 
                elinewidth=1.0,
                zorder = 1, label=f"$m={mi}$")
    
    if e == 0:
        label = "Theoretical value"
    else:
        label = "__nolegend__"
    
    # ax.plot(centres, theory,
    #               zorder = 2, linestyle="dashed", color="#444444",
    #               label = label)
    
ax.set_xlim(3e0, 2e1)

ax.vlines(np.log(1e4), 0, 2e0, color="#222222", linestyle="dashed",
          label="$\\log N$")

ax.set_xlabel("$k \\cdot \\left( \\log(m+1) - \\log m \\right)$")
yl = "$p(k) \\cdot \\left( \\frac{{m}}{{m+1}} \\right)^{{(m-k)}} \\cdot (m+1)$"
ax.set_ylabel(yl)
ax.legend()

fig.tight_layout(rect=(-0.02, -0.04, 0.98, 0.98))
fig.savefig("rand_m_collapse.eps")